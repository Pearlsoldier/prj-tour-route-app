from config.config import Config
from setup_contents import ContentsFormatter
from config.response_schema import GeminiResponse
from setup_system_prompt import SystemInstruction

from prompts import system_prompt, user_prompt

from client import GeminiClient


def main():
    chat_logs = []
    gemini_response = GeminiResponse
    formatted_contents = ContentsFormatter(
        user_prompt=user_prompt, chat_logs=[], user_input="東京駅近郊の観光地を教えて"
    )
    location_datasets = "東京タワーと東京駅、日比谷公園、皇居"

    gemini_system_instruction = SystemInstruction(
        system_instruction=system_prompt, location_datasets=location_datasets
    )
    gemini_config = Config(
        system_instruction=gemini_system_instruction.system_prompt,
        response_schema=gemini_response,
    )
    gemini_client = GeminiClient(
        config=gemini_config.setup_config,
        contents=formatted_contents.formatted_contents,
    )
    res = gemini_client.generate_response()
    print(res)
    print(f"返信内容: {res.parsed.response}")
    chat_logs.append(res.parsed.response)
    print(f"is_continue_conversation: {res.parsed.is_continue_conversation}")
    

if __name__ == "__main__":
    main()
