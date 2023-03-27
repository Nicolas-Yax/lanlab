from lanlab.tools.fun_tools import get_args_names
from lanlab.tools.list_tools import asym_diff
from lanlab.tools.dict_tools import SafeDict
from lanlab.tools.configurable import Configurable

import logging
import pickle
import os

class ModelConfig(SafeDict):
    def __init__(self):
        super().__init__()
        self.d['temperature'] = 1.
        self.d['max_tokens'] = 16
        self.d['top_p'] = 1
        self.d['stop'] = None
        self.d['logit_bias'] = None

class ModelInputConfig(ModelConfig):
    def __init__(self):
        super().__init__()
        self.d['prompt'] = None

class Model(Configurable):
    """ Language Model interface class """
    def __init__(self):
        super().__init__()
    def config_class(self):
        return ModelConfig
    def generate_input_config(self,prompt):
        input_dict = ModelInputConfig()
        input_dict.load_from(self.config)
        input_dict["prompt"] = prompt
        return input_dict
    def __call__(self,prompt):
        input_dict = self.generate_input_config(prompt)
        return self.ask(input_dict)
    def ask(self,input_config):
        raise NotImplementedError
    @property
    def surname(self):
        """ Name of the model (the short version if possible)"""
        return NotImplementedError
    def save(self,study):
        with open(os.path.join(study.path,'model.p'),'wb') as f:
            pickle.dump(self,f)

class OnlineModel(Model):
    """ Model ran online through an API that could bug sometimes"""
    def __init__(self):
        super().__init__()
        
        self.error_count = 0
        self.error_count_max = 20