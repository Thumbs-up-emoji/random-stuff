import os
from dotenv import load_dotenv

def main():
	load_dotenv()
	api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
	main()
