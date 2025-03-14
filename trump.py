import os
from mistralai import Mistral
from google import genai
from google.genai import types
from truthbrush import Api
from datetime import datetime, timedelta, timezone
import requests

def ask_mistral(msg):
    api_key = os.environ["MISTRAL_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "system",
                "content": "You are a busy professor of international political history, extremely knowledgable, very blunt, highly opinionated, and you don't take any bullshit. You tend to express your opinion in a rating from 1 to 10, with 10 being the worst possible thing a political leader could do, such as the Holocaust. A student is asking you about current events and specifically about public comments by the sitting president of the USA. Give a rating for his comment, and after that a small justification, don't be too lengthy. Consider as context other comments made by Donald Trump, especially from 2024 and 2025, and most importantly make extremely sure to point out factual errors.",
            },
            {
                "role": "user",
                "content": msg,
            },
        ]
    )
    print(chat_response.choices[0].message.content)


def ask_gemini(url):
    image_path=url
    image=requests.get(url)
    client=genai.Client(api_key=os.environ["GEMINI_KEY"])
    response=client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=["What is this image? Consider as context that you are a busy professor of international history, extremely knowledgable, very blunt, highly opinionated, and you don't take any bullshit. A student is asking you about current events and specifically about an image in a social media post by the US President. Just explain what's in the image simply.",
              types.Part.from_bytes(data=image.content, mime_type="image/jpeg")])
    print(response.text)

def main():
    u=os.environ["TS_UN"]
    p=os.environ["TS_PW"]
    client = Api(username=u, password=p)

    # Get datetime 24 hours ago using proper UTC timezone
    recent = datetime.now(timezone.utc) - timedelta(days=1)
    recent_statuses = client.pull_statuses(
        username="realDonaldTrump",
        created_after=recent
    )

    # Convert iterator to list once and store it
    statuses_list = list(recent_statuses)
    print(len(statuses_list))

    for status in statuses_list:
        print(status['content'])
        print("Posted at: ", status['created_at'])
        print("-------------------REVIEW STARTS HERE-------------------")
        for media in status['media_attachments']:
            print("________ABOUT THE IMAGE________")
            ask_gemini(media['url'])
            print("--------ON TO THE ATTACHED TEXT IF ANY--------")
        ask_mistral(status['content'])
        print("~~~~~Note that I can't actually go through videos/links, I might've just made something up actually~~~~~")
        print("_______________________________NEXT_______________________________")

if __name__ == "__main__":
   main()