import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Get the API key

print("API Key from .env:", api_key)  # Print the API key