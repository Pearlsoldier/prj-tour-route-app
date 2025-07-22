from config.response_schema import GeminiResponse
from google.genai import types


class Config:
    def __init__(self, system_instruction: str, response_schema: GeminiResponse):
        """
        configの設定、システムプロンプトと、構造化出力
        """
        self._system_instruction = system_instruction
        self._response_schema = response_schema

    @property
    def setup_config(self):
        return types.GenerateContentConfig(
            system_instruction=self._system_instruction,
            response_schema=self._response_schema,
        )
