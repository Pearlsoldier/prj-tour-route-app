from config.config import Config
from setup_contents import ContentsFormatter
from config.response_schema import GeminiResponse
from setup_system_prompt import SystemInstruction

from dialogue_prompts import dialogue_system_prompt, dialogue_user_prompt
from route_prompts import route_system_prompt, route_user_prompt

from model import Model

from client import GeminiClient

from google import genai
from google.genai import types


class ClientBuilder:

    @staticmethod
    def set_up_model():
        gemini_model = Model()
        return gemini_model.model

    @staticmethod
    def create_contents(user_input):
        formatted_contents = ContentsFormatter(
            user_prompt=user_prompt, user_input=user_input, chat_logs=[]
        )
        return formatted_contents

    @staticmethod
    def create_system_instruction(system_prompt, location_datasets=None):
        gemini_system_instruction = SystemInstruction(
            location_datasets,
            system_instruction=system_prompt,
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


class ChatInterface:
    def __init__(self, model, config, contents):
        """
        それぞれのクラスを受け取りそれらをまとめる（指揮）するクラスと考える
        """
        self._model = model
        self._config = config
        self._contents = contents
        self._client = GeminiClient(model, config, contents)
        self._chat_response = None

    def start_chat(self):
        self._chat_response = self._client.generate_response()
        return self._chat_response

    def continue_chat(self, new_user_input):
        self._contents.update_chat_logs(message=self._chat_response.parsed.response)
        self._contents.update_chat_logs(message=new_user_input)
        self._contents.update_user_input(new_user_input)
        self._client = GeminiClient(self._model, self._config, self._contents)
        self._chat_response = self._client.generate_response()
        return self._chat_response


# 使用方法
def main():
    user_input = "徒歩移動で東京駅から皇居外苑まで"
    builder = ClientBuilder
    gemini_model = builder.set_up_model()
    gemini_contents = builder.create_contents(user_input=user_input)
    gemini_system_prompt = builder.create_system_instruction()
    gemini_config = builder.create_config(
        gemini_system_instruction=gemini_system_prompt
    )

    gemini_chat = ChatInterface(
        model=gemini_model, config=gemini_config, contents=gemini_contents
    )
    chat = gemini_chat.start_chat()
    print(chat.parsed.response)
    print(chat.parsed.is_continue_conversation)


if __name__ == "__main__":
    main()
