import os
import requests
from mistralai import Mistral
from truthbrush import Api
from datetime import datetime, timedelta, timezone

def ask_mistral(msg):
    api_key = os.environ["MISTRAL_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "system",
                "content": "You are a busy professor of international political history, extremely knowledgable and also highly opinionated. You tend to express your opinion in a rating from 1 to 10, with 10 being the worst possible thing a political leader could do, such as the Holocaust. A student is asking you about current events and specifically about public comments by the sitting president of the USA. Give a rating for his comment, and after that a small justification, don't be too lengthy. Consider as context other comments made by Donald Trump, especially from 2024 and 2025",
            },
            {
                "role": "user",
                "content": msg,
            },
        ]
    )
    print(chat_response.choices[0].message.content)


def ask_gemini(url):
    print(url)
    return url

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
        ask_mistral(status['content'])

    # Check for media attachments and download them
    # if statuses_list[1]['media_attachments']:
    #     for idx, media in enumerate(statuses_list[1]['media_attachments']):
    #         media_url = media.get('url')
    #         ask_gemini(media_url)

if __name__ == "__main__":
    main()