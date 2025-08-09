from config.config import Config
from setup_contents import ContentsFormatter
from config.response_schema import GeminiResponse
from setup_system_prompt import SystemInstruction

from prompts import system_prompt, user_prompt

from client import GeminiClient


class ClientBuilder:
    @staticmethod
    def create_contents_format(user_input):
        formatted_contents = ContentsFormatter(
            user_prompt=user_prompt, user_input=user_input, chat_logs=[]
        )
        return formatted_contents

    @staticmethod
    def create_system_instruction(location_datasets):
        gemini_system_instruction = SystemInstruction(
            system_instruction=system_prompt, location_datasets=location_datasets
        )
        return gemini_system_instruction

    @staticmethod
    def create_config(gemini_system_instruction):
        gemini_response = GeminiResponse
        gemini_config = Config(
            system_instruction=gemini_system_instruction.system_prompt,
            response_schema=gemini_response,
        )
        return gemini_config

    @staticmethod
    def create_client(gemini_config, formatted_contents):
        gemini_client = GeminiClient(
            config=gemini_config.setup_config,
            contents=formatted_contents.formatted_contents,
        )
        return gemini_client


class ChatInterface:
    def __init__(self, client):
        """
        それぞれのクラスを受け取りそれらをまとめる（指揮）するクラスと考える
        """
        self._client = client

    def start_chat(self):
        res = self._client.generate_response()
        return res

    def continue_chat(self, new_user_input):
        """このインターフェースは状態を保つべきか？"""
        self._contents_format.update_chat_logs(message=user_input)
        self._contents_format.update_chat_logs(res.parsed.response)
        self._contents_format.update_user_input(new_user_input)


def main():
    chat = []
    user_input = "東京駅近郊の観光地を教えて"
