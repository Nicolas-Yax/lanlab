import os
import json

from lanlab.studies.study import Study
from lanlab.tools.dict_tools import SafeDict,to_dict
from lanlab.data_management.output.output_types.completion import Completion
from lanlab.data_management.output.output_collector.output_collector import OutputCollector

class OneModelStudyResults(OutputCollector):
    def __init__(self):
        self.data = []
        self.param_names = ['index_input','index_run']

    def add(self,q_index,input,output):
        try:
            self.data[q_index]
        except IndexError:
            self.data += [[] for i in range(len(self.data),q_index+1)]
        self.data[q_index].append({"input":input,"output":output})

    def dump_data(self):
        return to_dict(self.data)

    def load_data(self,d):
        self.data = d

class OneModelStudyConfig(SafeDict):
    def __init__(self):
        super().__init__()
        self.d["nb_run_per_question"] = 1
        self.d["append"] = ''
        self.d["prepend"] = ''

class OneModelStudy(Study):
    @property
    def config_class(self):
        return OneModelStudyConfig
    def load_output_collector(self):
        self.output_collector = OneModelStudyResults()
    def _run(self):
        max_adv = len(self.input_collector)*self['nb_run_per_question']
        for i,data in enumerate(self.input_collector):
            for j in range(self['nb_run_per_question']):
                print( str((i*self['nb_run_per_question']+j)/max_adv*100)[:2] +'%' ,end='\r')
                prompt = self['prepend']
                prompt += str(data)
                prompt += self['append']
                input_dict = self.model.generate_input_config(prompt)
                output_dict = self.model.ask(input_dict)
                self.output_collector.add(i,input_dict,output_dict)
        print('100%')
        
    @property
    def path(self):
        return os.path.join('data',self.name,self.model.name+'-'+self.input_collector.name)