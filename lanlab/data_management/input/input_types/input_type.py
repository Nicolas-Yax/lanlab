from lanlab.tools.configurable import Configurable
from lanlab.tools.dict_tools import SafeDict

class InputTypeConfig(SafeDict):
    pass

class InputType(Configurable):
    def config_class(self):
        return InputTypeConfig()
    def __str__(self):
        raise NotImplementedError