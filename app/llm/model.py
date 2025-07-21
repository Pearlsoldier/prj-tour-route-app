from google import genai


class Model:
    def __init__(self):
        self._model = "gemini-2.5-flash"

    @property
    def model(self):
        return self._model
