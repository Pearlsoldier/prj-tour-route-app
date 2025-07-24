from config.config import Config
from setup_user_prompt import UserPrompt
from config.response_schema import GeminiResponse
from setup_system_prompt import SystemInstruction

from prompts import system_prompt

from client import GeminiClient


def main():
    gemini_response = GeminiResponse
    user_prompt = UserPrompt(user_prompt=UserPrompt, chat_logs=[], user_input="東京駅近郊の観光地を教えて")
    location_datasets = "東京タワーと東京駅、日比谷公園、皇居"
    gemini_system_instruction = SystemInstruction(
        system_instruction=system_prompt, location_datasets=location_datasets
    )
    gemini_config = Config(system_instruction=gemini_system_instruction, response_schema=gemini_response)
    gemini_client = GeminiClient(config=gemini_config.setup_config)
    res = gemini_client.generate_response(user_input=user_prompt.user_prompt)
    print(res)
if __name__ == "__main__":
    main()
