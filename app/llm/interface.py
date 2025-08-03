from config.config import Config
from setup_contents import ContentsFormatter
from config.response_schema import GeminiResponse
from setup_system_prompt import SystemInstruction

from prompts import system_prompt, user_prompt

from client import GeminiClient

class llm_interface:
    def __init__(self, user_input):
        pass

    def llm_response(self):
        pass