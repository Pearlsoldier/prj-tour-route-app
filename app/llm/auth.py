import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


class AuthGemini:
    def __init__(self, api_key):
        self._api_key = api_key

    @property
    def get_gemini_api_key(self):
        return self._api_key
