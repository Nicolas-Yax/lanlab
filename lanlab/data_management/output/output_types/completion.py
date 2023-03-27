from lanlab.tools.dict_tools import SafeDict

class Completion(SafeDict):
    """ Normalized data type to represent a completion from a model"""
    def __init__(self):
        super().__init__()
        self.d['model'] = None
        self.d['tokens'] = []
        self.d['logp'] = []
        self.d['top_logp'] = []
        self.d['finish_reason'] = None