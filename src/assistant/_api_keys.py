import os
from dotenv import load_dotenv

load_dotenv()

class __APIKeys:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

AI_API_KEYS = __APIKeys()
