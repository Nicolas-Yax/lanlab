import logging

from lanlab.data_management.input.input_types.input_type import InputType,InputTypeConfig
from lanlab.tools.dict_tools import SafeDict

class QuestionConfig(InputTypeConfig):
    def __init__(self):
        super().__init__()
        self.d['format'] = 'Q:[prompt]\nA:'


class Question(InputType):
    def __init__(self,q=None):
        if q is None:
            q = {'prompt':None,'keywords':None,'info':None}
        self.from_dict(q)
        #Set initial config
        super().__init__()
    @property
    def config_class(self):
        return QuestionConfig
    def from_dict(self,q):
        self.prompt = q['prompt']
        self.keywords = q['keywords']
        self.info = q['info']
    def __str__(self):
        if not('[prompt]' in self['format']):
            logging.warning("[prompt] isn't detected in your question formatting :"+self['format']+".\n This will result in the actual input not being put in the prompt sent to the model.")
        s = str(self['format']).replace('[prompt]',self.prompt)
        return s