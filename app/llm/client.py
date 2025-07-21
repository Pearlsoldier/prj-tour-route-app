from google import genai
from auth import AuthGemini
from model import Model
from config.config import Config
from setup_user_prompt import UserPrompt

from config.response_schema import GeminiResponse
from setup_system_prompt import SystemPrompt


class GeminiClient:
    def __init__(self):
        self._gemini_model = Model().model
        self._contents = UserPrompt().user_prompt
        self._config = Config().setup_config
        self._setup_client()

    def _setup_client(self):
        auth = AuthGemini()
        self._gemini_api_key = auth.get_gemini_api_key
        self.client = genai.Client(api_key=self._gemini_api_key)

    def generate_response(self, user_input):
        response = self.client.models.generate_content(
            model=self._gemini_model, contents=self._contents, config=self._config
        )
        return response
