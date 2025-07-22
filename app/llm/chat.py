from config.config import Config
from setup_user_prompt import UserPrompt
from config.response_schema import GeminiResponse
from setup_system_prompt import SystemInstruction

from prompts import system_prompt

from client import GeminiClient


def main():

    location_datasets = "東京タワーと東京駅、日比谷公園、皇居"
    gemini_system_instruction = SystemInstruction(
        system_instruction=system_prompt, location_datasets=location_datasets
    )
    print(gemini_system_instruction.system_prompt)


if __name__ == "__main__":
    main()
