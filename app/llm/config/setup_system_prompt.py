class SystemInstruction:
    def __init__(self, system_instruction, **kwargs):
        self._base_prompt = system_instruction
        self._params = kwargs
        self._location_datasets = kwargs.get('location_datasets', [])
        self._system_prompt = self._setup_prompt()

    def _setup_prompt(self):
        self.locations = self._location_datasets
        return self._base_prompt.format(**self._params)
    
    @property
    def system_prompt(self):
        return self._system_prompt
