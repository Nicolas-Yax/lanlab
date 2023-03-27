import pandas as pd
import json
import os

from lanlab.data_management.output.output_types.completion import Completion
from lanlab.data_management.output.output_collector.output_collector import OutputCollector

class Results(OutputCollector):
    def __init__(self,param_names):
        self.data = {}
        self.param_names = param_names

    def add(self,entry_label,input,output):
        self.data[str(entry_label)] = {"input":input,"output":output}

    def dump_data(self):
        d = {}
        for k in self.data:
            d[k] = {"input":self.data[k]["input"].to_dict(),"output":self.data[k]["output"].to_dict()}
        return d

    def load_data(self,d):
        self.data = {}
        for k in d:
            self.data[k] = {"input":d[k]["input"],"output":d[k]["output"]}

    def save_data(self,study):
        with open(os.path.join(study.path,"data.json"),'w') as f:
            json.dump(self.dump_data(),f)