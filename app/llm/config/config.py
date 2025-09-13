class Config:
    """
    システムプロンプトとレスポンススキームは必ず必要なので、引数としてセットする。
    これは汎用的にしようできる。
    """

    def __init__(self, system_instruction, response_schema):
        """
        configの設定、システムプロンプトと、構造化出力
        """
        self._system_instruction = system_instruction
        self._response_schema = response_schema

    @property
    def setup_config(self):
        return {
            "system_instruction": self._system_instruction,
            "response_mime_type": "application/json",
            "response_schema": self._response_schema,
        }
