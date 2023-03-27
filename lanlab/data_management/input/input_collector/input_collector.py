import pickle
import os

from lanlab.tools.configurable import Configurable
from lanlab.data_management.input.input_types.input_type import InputTypeConfig

class InputCollector(Configurable):
    @property
    def config_class(self):
        return InputTypeConfig
    def __iter__(self):
        raise NotImplementedError