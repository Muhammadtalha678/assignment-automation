from dotenv import load_dotenv
import os

load_dotenv()

model_name = os.getenv("model_name")
base_url = os.getenv("base_url")
api_key = os.getenv("api_key")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")