class SystemPrompt:
    def __init__(self, system_prompt, location_datas):
        self._base_prompt = system_prompt
        self._location_datas = location_datas
        self._system_prompt = self._setup_prompt()

    def _setup_prompt(self):
        self.locations = self._location_datas
        return self._base_prompt.format(location_data=self.locations)

    @property
    def system_prompt(self):
        return self._system_prompt
