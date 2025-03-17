import requests
from google import genai
from google.genai import types
import os

try:
    # URL for a sample image
    image_url = "https://picsum.photos/800/600"  # Random image from Lorem Picsum
    
    # Fetch the image from the URL
    response = requests.get(image_url)
    response.raise_for_status()  # Raise exception for 4XX/5XX responses
    image_bytes = response.content
    
    # Initialize Gemini client
    client = genai.Client(api_key=os.environ["GEMINI_KEY"])
    
    # Send the image to Gemini for analysis
    gemini_response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[
            "What is shown in this image? Please describe it in detail.",
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
        ]
    )
    
    # Print the response
    print(f"Image URL: {image_url}")
    print(f"Gemini response:\n{gemini_response.text}")
    
except Exception as e:
    print(f"Error: {str(e)}")