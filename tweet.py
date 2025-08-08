import tweepy
import os
import json
from datetime import datetime
from trump import ask_gemini, ask_mistral

# bearer_token = os.environ["X_BEARER_TOKEN"]
bearer_token="AAAAAAAAAAAAAAAAAAAAAPoH2AEAAAAAdxfnp%2BDruKGywaYYrb49UBiANUs%3DW60Ige7csONJhWrcacWbQrjRpAS7goFgf5LpLUBrXiI84ZxVdl"
# print(bearer_token)
client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

def fetch_tweets(user_choice):
    """
    Fetch tweets from a selected Twitter user and save as JSON.
    
    Args:
        user_choice: String or integer representing user selection (1-4)
    """
    # Convert to string in case an int is passed
    user_choice = str(user_choice)
    
    # Define available user IDs with their descriptions
    user_ids = {
        "1": {"id": 1879644163769335808, "name": "White House"},
        "2": {"id": 25073877, "name": "Donald Trump"},
        "3": {"id": 1856751787644260354, "name": "DOGE"},
        "4": {"id": 44196397, "name": "Elon Musk"}
    }
    
    # Validate selection and get the user_id
    if user_choice in user_ids:
        selected_user = user_ids[user_choice]
        user_id = selected_user["id"]
        print(f"\nFetching tweets for {selected_user['name']}...\n")
    else:
        print("Invalid selection. Using default (White House).")
        user_id = user_ids["1"]["id"]
        selected_user = user_ids["1"]
    
    # Get User's Tweets, expanding attachments and referenced tweets
    response = client.get_users_tweets(
        user_id, 
        user_auth=False, 
        max_results=5,
        expansions=["referenced_tweets.id", "attachments.media_keys", "in_reply_to_user_id"],
        tweet_fields=["entities", "attachments", "in_reply_to_user_id"],
        media_fields=["url", "type"]
    )
    
    # Create lookup dictionaries for included data
    included_tweets = {tweet.id: tweet for tweet in response.includes['tweets']} if response.includes and 'tweets' in response.includes else {}
    included_media = {media.media_key: media for media in response.includes['media']} if response.includes and 'media' in response.includes else {}

    # Prepare data structure for JSON
    tweets_data = {
        "user": selected_user["name"],
        "user_id": user_id,
        "fetched_at": datetime.now().isoformat(),
        "tweets": []
    }
    
    # Collect tweet data
    for tweet in response.data:
        text = tweet.text
        
        tweet_info = {
            "id": str(tweet.id),
            "text": text,
            "in_reply_to": None,
            "links": [],
            "media": []
        }

        # Check for referenced tweets (retweets, replies, quotes)
        if tweet.referenced_tweets:
            for ref_tweet in tweet.referenced_tweets:
                original_tweet_id = ref_tweet.id
                original_tweet = included_tweets.get(original_tweet_id)

                if not original_tweet:
                    continue

                if ref_tweet.type == 'retweeted':
                    # Prepend RT and original author info to the text
                    text = f"RT: {original_tweet.text}"
                    tweet_info["text"] = text # Update text in our dict
                
                elif ref_tweet.type == 'replied_to':
                    tweet_info["in_reply_to"] = {
                        "tweet_id": str(original_tweet.id),
                        "text": original_tweet.text
                    }
        
        # Extract and classify URLs from entities
        if tweet.entities and 'urls' in tweet.entities:
            for url_entity in tweet.entities['urls']:
                # If the URL is for media, it will be handled below
                if 'media_key' not in url_entity:
                    link_info = {
                        "url": url_entity['url'],
                        "expanded_url": url_entity['expanded_url'],
                        "display_url": url_entity['display_url']
                    }
                    tweet_info["links"].append(link_info)

        # Extract media attachments
        if tweet.attachments and 'media_keys' in tweet.attachments:
            for media_key in tweet.attachments['media_keys']:
                if media_key in included_media:
                    media_item = included_media[media_key]
                    media_info = {
                        "type": media_item.type,
                        "media_key": media_item.media_key
                    }
                    if media_item.type == 'photo' and hasattr(media_item, 'url'):
                        media_info['url'] = media_item.url
                    tweet_info["media"].append(media_info)

        tweets_data["tweets"].append(tweet_info)
        print(f"Tweet ID: {tweet.id}")
        print(f"Text: {text}")
        # Print reply info
        if tweet_info["in_reply_to"]:
            print(f"  -> In reply to: \"{tweet_info['in_reply_to']['text'][:70]}...\"")
        # Print detected media and links
        for media in tweet_info["media"]:
            print(f"  -> Media Type: {media['type']}")
        for link in tweet_info["links"]:
            print(f"  -> Article/Link: {link['expanded_url']}")
        
        # AI Analysis Section
        print("\n" + "-" * 20 + " AI ANALYSIS " + "-" * 20)
        # Analyze images with Gemini
        if tweet_info["media"]:
            for media in tweet_info["media"]:
                if media.get('type') == 'photo' and 'url' in media:
                    print(f"\n--- Analyzing image: {media['url']} ---")
                    ask_gemini(media['url'])
        
        # Analyze text with Mistral
        print("\n--- Analyzing text ---")
        ask_mistral(text)
        print("-" * 50)
    
    # Save to JSON file
    filename = "tweets.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweets_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nTweets saved to {filename}")
    return tweets_data


# Example usage
if __name__ == "__main__":
    print("Select a Twitter user to fetch tweets from:")
    print("1: White House")
    print("2: Donald Trump")
    print("3: DOGE")
    print("4: Elon Musk")
    
    selection = input("Enter your choice (1-4): ")
    fetch_tweets(selection)