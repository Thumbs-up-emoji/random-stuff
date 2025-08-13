import os
from mistralai import Mistral
from google import genai
from google.genai import types
from truthbrush import Api
from datetime import datetime, timedelta, timezone
import requests
import re

# Set up logging to a file
log_filename = "trump_analysis.txt"
log_file = open(log_filename, "w", encoding="utf-8")

def log_print(message):
    """Print to both console and log file"""
    print(message)
    log_file.write(f"{message}\n")
    log_file.flush()  # Force write to disk

def is_empty_content(content):
    """Check if content is empty or just contains HTML tags with no text"""
    if not content:
        return True
    
    # Remove all HTML tags
    no_html = re.sub(r'<[^>]*>', '', content)
    
    # Check if what remains is just whitespace
    if not no_html.strip():
        return True
    
    return False

def ask_mistral(msg):
    try:
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
        if chat_response.choices and getattr(chat_response.choices[0], "message", None) and getattr(chat_response.choices[0].message, "content", None):
            log_print(chat_response.choices[0].message.content)
        else:
            log_print("No response content received from Mistral.")
    except Exception as e:
        log_print(f"Error in ask_mistral: {str(e)}")


def ask_gemini(url):
    try:
        image = requests.get(url)
        client = genai.Client(api_key=os.environ["GEMINI_KEY"])
        response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=["What is this image? Consider as context that you are a professor of international history, highly opinionated, helpful but you keep your answers short. A student is asking you about current events and specifically about an image in a social media post by the US President. Just explain what's in the image simply.",
                types.Part.from_bytes(data=image.content, mime_type="image/jpeg")])
        log_print(response.text)
    except Exception as e:
        log_print(f"Error processing image at {url}: {str(e)}")

def main():
    try:
        u = os.environ["TS_UN"]
        p = os.environ["TS_PW"]
        client = Api(token=os.environ["TS_TOKEN"])

        # Get datetime 24 hours ago using proper UTC timezone
        recent = datetime.now(timezone.utc) - timedelta(days=1)
        recent_statuses = client.pull_statuses(
            username="realDonaldTrump",
            created_after=recent
        )

        # Convert iterator to list once and store it
        try:
            statuses_list = list(recent_statuses)
            log_print(f"Found {len(statuses_list)} recent posts")
        except Exception as e:
            log_print(f"Error fetching statuses: {str(e)}")
            statuses_list = []

        i=1
        for status in statuses_list:
            try:
                log_print(f"Status {i}")
                i += 1
                log_print(status['content'])
                log_print(f"Posted at: {status['created_at']}")
                log_print("-------------------REVIEW STARTS HERE-------------------")
                
                if 'media_attachments' in status and status['media_attachments']:
                    for media in status['media_attachments']:
                        try:
                            log_print("________ABOUT THE IMAGE________")
                            log_print(media['url'])
                            ask_gemini(media['url'])
                        except Exception as e:
                            log_print(f"Error processing media attachment: {str(e)}")
                    log_print("--------ON TO THE ATTACHED TEXT IF ANY--------")
                
                # Only call Mistral if there's actual content
                if not is_empty_content(status['content']):
                    ask_mistral(status['content'])
                else:
                    log_print("No text content to analyze - skipping text analysis")
                
                log_print("~~~~~Note that I can't actually go through videos/links, I might've just made something up actually (especially if there is no text given)~~~~~")
                log_print("_______________________________NEXT_______________________________")
            except Exception as e:
                log_print(f"Error processing status: {str(e)}")
                log_print("_______________________________NEXT_______________________________")
                continue
                
    except Exception as e:
        log_print(f"Fatal error in main: {str(e)}")
    finally:
        # Log completion message before closing the file
        log_print(f"Analysis complete. Log saved to {log_filename}")
        # Now close the file
        log_file.close()

if __name__ == "__main__":
    try:
        # Log the start time
        start_time = datetime.now()
        log_print(f"Trump analysis started at {start_time}")
        
        main()
        
        # Log the end time and duration
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"Analysis completed at {end_time}")  # Use regular print here
        print(f"Total duration: {duration}")  # Use regular print here
    except Exception as e:
        print(f"Unhandled exception: {str(e)}")  # Use regular print here