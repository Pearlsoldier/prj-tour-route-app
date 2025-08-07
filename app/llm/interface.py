from config.config import Config
from setup_contents import ContentsFormatter
from config.response_schema import GeminiResponse
from setup_system_prompt import SystemInstruction

from prompts import system_prompt, user_prompt

from client import GeminiClient


class ChatInterface:
    def __init__(self, client, config, format):
        """
        それぞれのクラスを受け取りそれらをまとめる（指揮）するクラスと考える
        """
        self._client = client
        self._config = config
        self._contents_format = format
    
    def start_chat(self):
        res = self._client.generate_response()
        return res

    def continue_chat(self, new_user_input):
        """このインターフェースは状態を保つべきか？"""
        self._contents_format.update_chat_logs(message=user_input)
        self._contents_format.update_chat_logs(res.parsed.response)
        self._contents_format.update_user_input(new_user_input)


