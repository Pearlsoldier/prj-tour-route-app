class ContentsFormatter:
    def __init__(
        self,
        user_prompt,
        user_input,
        chat_logs=None,
    ):
        self._user_prompt = user_prompt
        self._chat_logs = chat_logs
        self._user_input = user_input
        self._con = self._setup_prompt()

    def _setup_prompt(self):
        return self._user_prompt.format(
            chat_logs=self._chat_logs, user_input=self._user_input
        )

    def update_chat_logs(self, message):
        self._chat_logs.append(message)

    def update_user_input(self, user_input):
        self._user_input = user_input

    @property
    def formatted_contents(self):
        content_text = self._setup_prompt()
        return [types.UserContent(parts=[types.Part.from_text(text=content_text)])]
