import os
from dotenv import load_dotenv


class AuthGemini:
    def __init__(self):
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self._api_key = GEMINI_API_KEY

    @property
    def get_gemini_api_key(self):
        return self._api_key
