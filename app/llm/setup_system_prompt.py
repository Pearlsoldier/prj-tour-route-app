class SystemInstruction:
    def __init__(self, system_instruction, location_datasets):
        self._base_prompt = system_instruction
        self._location_datasets = location_datasets
        self._system_prompt = self._setup_prompt()

    def _setup_prompt(self):
        self.locations = self._location_datasets
        return self._base_prompt.format(location_datasets=self.locations)

    @property
    def system_prompt(self):
        return self._system_prompt
