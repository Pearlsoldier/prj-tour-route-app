from google import genai


class Model:
    def __init__(self):
        self._model = "gemini-2.5-flash"

    @property
    def get_model(self):
        return self._model


def __main__():
    gemini = Model()
    print(gemini.get_model)


if __name__ == "__main__":
    __main__()
