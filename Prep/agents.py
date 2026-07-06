import csv
import math
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph


RACES_FILE = Path(__file__).with_name("allowed_races.csv")
MAX_RACE_ATTEMPTS = 2
MAX_NAME_ATTEMPTS = 2


class VillainState(TypedDict, total=False):
    villain_ideas: str
    allowed_races: list[str]
    retrieved_races: list[dict[str, object]]
    race_context: str
    race: str
    race_attempt: int
    race_valid: bool
    race_feedback: str
    race_validation_history: list[dict[str, object]]
    names: str
    attempt: int
    evaluation: str
    passed: bool
    feedback: str
    attempts_history: list[dict[str, object]]


def print_step(title, text):
    print(f"\n{title}")
    print("-" * len(title))
    print(text)


def cosine_similarity(left_vector, right_vector):
    numerator = sum(left * right for left, right in zip(left_vector, right_vector))
    left_magnitude = math.sqrt(sum(left * left for left in left_vector))
    right_magnitude = math.sqrt(sum(right * right for right in right_vector))

    if left_magnitude == 0 or right_magnitude == 0:
        return 0.0

    return numerator / (left_magnitude * right_magnitude)


def load_allowed_races():
    with RACES_FILE.open(newline="", encoding="utf-8") as race_file:
        reader = csv.DictReader(race_file)

        if not reader.fieldnames:
            raise ValueError(f"{RACES_FILE.name} must contain a header row with a race column.")

        columns = {column.strip().lower(): column for column in reader.fieldnames}
        race_column = columns.get("race") or columns.get("name")
        description_column = columns.get("description") or columns.get("notes")

        if not race_column:
            raise ValueError(f"{RACES_FILE.name} must contain a race or name column.")

        races = []
        for row in reader:
            race = (row.get(race_column) or "").strip()
            description = (row.get(description_column) or "").strip() if description_column else ""

            if race:
                races.append({"race": race, "description": description})

    if not races:
        raise ValueError(f"{RACES_FILE.name} must contain at least one allowed race.")

    return races


def build_race_documents(races):
    documents = []

    for race_info in races:
        description = race_info["description"]
        document_text = f"Race: {race_info['race']}\nDescription: {description}" if description else f"Race: {race_info['race']}"
        documents.append({
            "race": race_info["race"],
            "description": description,
            "text": document_text,
        })

    return documents


def embed_race_documents(embeddings, race_documents):
    texts = [document["text"] for document in race_documents]
    vectors = embeddings.embed_documents(texts)

    return [
        {
            **document,
            "vector": vector,
        }
        for document, vector in zip(race_documents, vectors)
    ]


def retrieve_races(query, embeddings, embedded_race_documents, top_k=3):
    query_vector = embeddings.embed_query(query)
    ranked_documents = sorted(
        embedded_race_documents,
        key=lambda document: cosine_similarity(query_vector, document["vector"]),
        reverse=True,
    )

    retrieved_documents = []
    for document in ranked_documents[:top_k]:
        retrieved_documents.append(
            {
                "race": document["race"],
                "description": document["description"],
                "score": cosine_similarity(query_vector, document["vector"]),
            }
        )

    return retrieved_documents


def format_race_context(races):
    lines = []

    for race_info in races:
        race = race_info["race"]
        description = race_info["description"]
        lines.append(f"- {race}: {description}" if description else f"- {race}")

    return "\n".join(lines)


def normalize_race_name(race):
    return " ".join(race.lower().replace("-", " ").split())


def validate_race_from_document(race, allowed_races):
    cleaned_race = race.strip().splitlines()[0].strip(" .,:;\"'")
    allowed_lookup = {normalize_race_name(allowed_race): allowed_race for allowed_race in allowed_races}
    matched_race = allowed_lookup.get(normalize_race_name(cleaned_race))

    if matched_race:
        return matched_race, True, f"{matched_race} is listed in {RACES_FILE.name}."

    allowed_text = ", ".join(allowed_races)
    return (
        cleaned_race,
        False,
        f"{cleaned_race} is not listed in {RACES_FILE.name}. Choose exactly one of: {allowed_text}.",
    )


def format_retrieved_races(races):
    lines = []

    for race_info in races:
        description = race_info["description"]
        score = race_info["score"]
        lines.append(
            f"- {race_info['race']} (score={score:.3f})"
            + (f": {description}" if description else "")
        )

    return "\n".join(lines)


def parse_evaluation(evaluation):
    passed = False
    feedback = "No feedback provided."

    for line in evaluation.splitlines():
        label, _, value = line.partition(":")
        label = label.strip().lower()
        value = value.strip()

        if label == "pass":
            passed = value.lower() == "yes"
        elif label == "feedback":
            feedback = value

    return passed, feedback


def build_chains(llm, parser):
    villain_ideas_chain = (
        ChatPromptTemplate.from_template("Give me 5 interesting fantasy villain concepts.")
        | llm
        | parser
    )

    race_picker_chain = (
        ChatPromptTemplate.from_template(
            "Based on these fantasy villain concepts, suggest exactly one fantasy race "
            "that would be interesting for a villain.\n\n"
            "Concepts:\n{villain_ideas}\n\n"
            "Retrieved allowed races from the CSV:\n{race_context}\n\n"
            "Validation feedback from previous attempt, if any:\n{race_feedback}\n\n"
            "Return only one race name exactly as it appears in the retrieved races."
        )
        | llm
        | parser
    )

    names_chain = (
        ChatPromptTemplate.from_template(
            "Give me 5 uninteresting and cliche names for fantasy villains whose race is {race}.\n\n"
            "Feedback to incorporate, if any:\n{feedback}"
        )
        | llm
        | parser
    )

    rating_chain = (
        ChatPromptTemplate.from_template(
            "You are rating fantasy villain names.\n\n"
            "Race: {race}\n\n"
            "Names:\n{names}\n\n"
            "Rate each name from 1 to 10. Be extremely strict. The list only passes if every name is at least 8/10.\n"
            "Return exactly this format:\n"
            "PASS: yes or no\n"
            "LOWEST_SCORE: number\n"
            "FEEDBACK: one short sentence explaining what to improve if PASS is no, "
            "or why the list passed if PASS is yes."
        )
        | llm
        | parser
    )

    return villain_ideas_chain, race_picker_chain, names_chain, rating_chain


def run_langchain_flow(villain_ideas_chain, race_picker_chain, names_chain):
    print("\nLANGCHAIN VERSION")
    print("=======================")

    allowed_race_rows = load_allowed_races()
    allowed_races = [race_info["race"] for race_info in allowed_race_rows]
    race_documents = build_race_documents(allowed_race_rows)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    embedded_race_documents = embed_race_documents(embeddings, race_documents)

    villain_ideas = villain_ideas_chain.invoke({})
    print_step("Step 1: Fantasy Villain Concepts", villain_ideas)

    retrieved_races = retrieve_races(villain_ideas, embeddings, embedded_race_documents)
    race_context = format_retrieved_races(retrieved_races)

    race = race_picker_chain.invoke(
        {
            "villain_ideas": villain_ideas,
            "race_context": race_context,
            "race_feedback": "No previous validation feedback.",
        }
    ).strip()
    race, race_valid, race_feedback = validate_race_from_document(race, allowed_races)
    print_step("Step 2: Chosen Race", race)
    print_step("Step 2 Validation", race_feedback)

    if not race_valid:
        race = allowed_races[0]
        print(f"Using fallback race for linear LangChain flow: {race}")

    names = names_chain.invoke(
        {
            "race": race,
            "feedback": "No previous feedback. This is the first attempt.",
        }
    )
    print_step(f"Step 3: Names For {race} Villains", names)


def run_langgraph_flow(villain_ideas_chain, race_picker_chain, names_chain, rating_chain):
    print("\nLANGGRAPH VERSION")
    print("=================")

    def generate_villain_ideas(state: VillainState):
        villain_ideas = villain_ideas_chain.invoke({})
        return {"villain_ideas": villain_ideas}

    def retrieve_allowed_races(state: VillainState):
        allowed_race_rows = load_allowed_races()
        race_documents = build_race_documents(allowed_race_rows)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        embedded_race_documents = embed_race_documents(embeddings, race_documents)
        retrieved_races = retrieve_races(state["villain_ideas"], embeddings, embedded_race_documents)
        return {
            "allowed_races": [race_info["race"] for race_info in allowed_race_rows],
            "retrieved_races": retrieved_races,
            "race_context": format_retrieved_races(retrieved_races),
        }

    def pick_race(state: VillainState):
        race_attempt = state.get("race_attempt", 0) + 1
        race_feedback = state.get("race_feedback", "No previous validation feedback.")
        race = race_picker_chain.invoke(
            {
                "villain_ideas": state["villain_ideas"],
                "race_context": state["race_context"],
                "race_feedback": race_feedback,
            }
        ).strip()
        return {"race_attempt": race_attempt, "race": race}

    def validate_race(state: VillainState):
        race, race_valid, race_feedback = validate_race_from_document(
            state["race"],
            state["allowed_races"],
        )
        race_validation_history = state.get("race_validation_history", []) + [
            {
                "attempt": state["race_attempt"],
                "race": race,
                "passed": race_valid,
                "feedback": race_feedback,
            }
        ]

        return {
            "race": race,
            "race_valid": race_valid,
            "race_feedback": race_feedback,
            "race_validation_history": race_validation_history,
        }

    def use_fallback_race(state: VillainState):
        fallback_race = state["allowed_races"][0]
        race_feedback = f"Using fallback race {fallback_race} after invalid race selections."
        race_validation_history = state.get("race_validation_history", []) + [
            {
                "attempt": "fallback",
                "race": fallback_race,
                "passed": True,
                "feedback": race_feedback,
            }
        ]

        return {
            "race": fallback_race,
            "race_valid": True,
            "race_feedback": race_feedback,
            "race_validation_history": race_validation_history,
        }

    def generate_names(state: VillainState):
        attempt = state.get("attempt", 0) + 1
        feedback = state.get("feedback", "No previous feedback. This is the first attempt.")
        names = names_chain.invoke({"race": state["race"], "feedback": feedback})
        return {"attempt": attempt, "names": names}

    def rate_names(state: VillainState):
        evaluation = rating_chain.invoke({"race": state["race"], "names": state["names"]})
        passed, feedback = parse_evaluation(evaluation)
        attempts_history = state.get("attempts_history", []) + [
            {
                "attempt": state["attempt"],
                "names": state["names"],
                "evaluation": evaluation,
                "feedback": feedback,
                "passed": passed,
            }
        ]

        return {
            "evaluation": evaluation,
            "passed": passed,
            "feedback": feedback,
            "attempts_history": attempts_history,
        }

    def choose_next_step(state: VillainState):
        if state["passed"] or state["attempt"] >= MAX_NAME_ATTEMPTS:
            return "stop"

        return "retry"

    def choose_after_race_validation(state: VillainState):
        if state["race_valid"]:
            return "valid"

        if state["race_attempt"] >= MAX_RACE_ATTEMPTS:
            return "fallback"

        return "retry"

    graph_builder = StateGraph(VillainState)
    graph_builder.add_node("generate_villain_ideas", generate_villain_ideas)
    graph_builder.add_node("retrieve_allowed_races", retrieve_allowed_races)
    graph_builder.add_node("pick_race", pick_race)
    graph_builder.add_node("validate_race", validate_race)
    graph_builder.add_node("use_fallback_race", use_fallback_race)
    graph_builder.add_node("generate_names", generate_names)
    graph_builder.add_node("rate_names", rate_names)

    graph_builder.set_entry_point("generate_villain_ideas")
    graph_builder.add_edge("generate_villain_ideas", "retrieve_allowed_races")
    graph_builder.add_edge("retrieve_allowed_races", "pick_race")
    graph_builder.add_edge("pick_race", "validate_race")
    graph_builder.add_conditional_edges(
        "validate_race",
        choose_after_race_validation,
        {
            "retry": "pick_race",
            "fallback": "use_fallback_race",
            "valid": "generate_names",
        },
    )
    graph_builder.add_edge("use_fallback_race", "generate_names")
    graph_builder.add_edge("generate_names", "rate_names")
    graph_builder.add_conditional_edges(
        "rate_names",
        choose_next_step,
        {
            "retry": "generate_names",
            "stop": END,
        },
    )

    graph = graph_builder.compile()
    final_state = graph.invoke({})

    print_step("Step 1: Fantasy Villain Concepts", final_state["villain_ideas"])
    print_step("Step 2: Retrieved Allowed Race Context", final_state["race_context"])
    print_step("Step 3: Race Selection Validation", "")

    for race_attempt in final_state["race_validation_history"]:
        print(f"Race attempt {race_attempt['attempt']}: {race_attempt['race']}")
        print(f"Valid: {race_attempt['passed']}")
        print(f"Feedback: {race_attempt['feedback']}")
        print()

    print_step(
        f"Step 4: Final Names For {final_state['race']} Villains",
        final_state["names"],
    )
    print_step("Step 5: Name Attempt History", "")

    for attempt_result in final_state["attempts_history"]:
        print(f"Attempt {attempt_result['attempt']}")
        print("-" * 9)
        print("Names:")
        print(attempt_result["names"])
        print("\nRating:")
        print(attempt_result["evaluation"])
        print(f"\nFeedback for next attempt: {attempt_result['feedback']}")
        print(f"Passed: {attempt_result['passed']}")
        print()

    print(f"\nName generation attempts used: {final_state['attempt']} of {MAX_NAME_ATTEMPTS}")


def main():
    load_dotenv()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    parser = StrOutputParser()
    villain_ideas_chain, race_picker_chain, names_chain, rating_chain = build_chains(llm, parser)

    # run_langchain_flow(villain_ideas_chain, race_picker_chain, names_chain)
    run_langgraph_flow(villain_ideas_chain, race_picker_chain, names_chain, rating_chain)
    
if __name__ == "__main__":
    main()
