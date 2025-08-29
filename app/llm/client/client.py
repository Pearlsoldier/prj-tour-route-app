import google.generativeai as genai
from llm.auth.auth import AuthGemini
from llm.model.model import Model
from llm.config.setup_contents import ContentsFormatter


class GeminiClient:
    def __init__(self, model, config, contents):
        self._gemini_model = model
        self._contents = contents
        self._config = config
        self._setup_client()
        self._chat_response = None

    def _setup_client(self):
        auth = AuthGemini()
        self._gemini_api_key = auth.get_gemini_api_key
        genai.configure(api_key=self._gemini_api_key)

    def generate_response(self):
        model = genai.GenerativeModel(
            model_name=self._gemini_model,
            system_instruction=self._config.setup_config.get('system_instruction', '')
        )
        # GenerationConfigからsystem_instructionを除去
        generation_config = {k: v for k, v in self._config.setup_config.items() if k != 'system_instruction'}
        
        return model.generate_content(
            contents=self._contents.formatted_contents,
            generation_config=generation_config,
        )
