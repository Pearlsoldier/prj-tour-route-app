import os

from dotenv import load_dotenv

class GeminiSecrets:
    def __init__(self) -> None:
        self.__api_key = load_local_env()
    
    @property
    def api_key(self) -> str:
        return self.__api_key
    
    def load_local_env()
        