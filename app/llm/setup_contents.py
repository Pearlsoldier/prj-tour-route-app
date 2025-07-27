class ContentsFormatter:
    def __init__(self, user_prompt, chat_logs, user_input):
        self._user_prompt = user_prompt
        self._chat_logs = chat_logs
        self._user_input = user_input
        self._con = self._setup_prompt()

    def _setup_prompt(self):
        return self._user_prompt.format(
            chat_logs=self._chat_logs, user_input=self._user_input
        )

    @property
    def formatted_contents(self):
        return self._user_prompt
