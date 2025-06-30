class GeminiConfig:
    def __init__(self):
        pass

    @property
    def api_version(self) -> str:
        return "2024-07-01-preview"

    @property
    def azure_endpoint(self) -> str:
        return "https://dev1-di-a3-japaneast.openai.azure.com/"

    @property
    def gemini_20_flash(self) -> str:
        """
        model = "deployment_name".
        """
        return "gemini-2.0-flash"
