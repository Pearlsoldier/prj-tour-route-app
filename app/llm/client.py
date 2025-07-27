from google import genai
from auth import AuthGemini
from model import Model
from setup_contents import ContentsFormatter


class GeminiClient:
    def __init__(self, config, contents):
        self._gemini_model = Model().model
        self._contents = contents
        self._config = config
        self._setup_client()

    def _setup_client(self):
        auth = AuthGemini()
        self._gemini_api_key = auth.get_gemini_api_key
        self.client = genai.Client(api_key=self._gemini_api_key)

    def generate_response(self):
        response = self.client.models.generate_content(
            model=self._gemini_model, contents=self._contents, config=self._config
        )
        return response
