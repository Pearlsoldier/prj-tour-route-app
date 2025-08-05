from config.config import Config
from setup_contents import ContentsFormatter
from config.response_schema import GeminiResponse
from setup_system_prompt import SystemInstruction

from prompts import system_prompt, user_prompt

from client import GeminiClient


class ChatInterface:
    def __init__(
        self,
        response_schema,
        contents_formatter,
        client,
        system_instruction,
        user_input,
        chat_logs,
    ):
        self._response_schema = response_schema
        self._contents_formatter = contents_formatter
        self._client = client
        self._system_instruction = system_instruction
        self._user_input = user_input
        self._chat_logs = chat_logs
