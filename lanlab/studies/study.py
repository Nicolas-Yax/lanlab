import os
import logging
import json
import pickle

from lanlab.tools.dict_tools import SafeDict
from lanlab.tools.configurable import Configurable

class UnnamedStudy(Exception):
    """ Raised when something tries to access the study name but the name is not defined """
    def __init__(self):
        self.message = "The study has no name. However it is mandatory to name is as it is required to initialize the files related to this study. You can name the study using the name=[your study name] parameter when creating the object or by heritage by overloading the @property name."

class StudyConfig(SafeDict):
    pass

class Study(Configurable):
    def __init__(self,input_collector,model,name=None):
        self.input_collector = input_collector
        self.model = model
        self._name = name
        self.load_output_collector()
        super().__init__()
    def load_output_collector(self):
        raise NotImplementedError
    @property
    def config_class(self):
        return StudyConfig
    def already_exists(self):
        return os.path.isdir(self.path)
    def create_folders(self):
        os.makedirs(self.path)
    def run(self,update_objects=False,update_data=False):
        if self.already_exists():
            logging.info("Found the study. Trying to load it and the data.")
            self.load(load_objects=not(update_objects),load_data=not(update_data))
            if update_objects:
                logging.info('Study successfully partially loaded')
                self.save()
            if update_data:
                logging.info('Study successfully partially loaded')
                self._run()
                self.save()
            else:
                logging.info('Study successfully loaded')
        else:
            logging.info("Didn't find the study. Running it.")
            self.create_folders()
            self._run()
            self.save()
    @property
    def name(self):
        if self._name is None:
            assert UnnamedStudy() #Name of study not defined.
        return self._name
    @property
    def path(self):
        raise NotImplementedError

    def save(self):
        self.output_collector.save_data(self)
        with open(os.path.join(self.path,'study.p'),'wb') as f:
            d = self.output_collector.pop_data()
            pickle.dump(self,f)
            self.output_collector.set_data(d)

    def load(self,load_objects=False,load_data=False):
        if load_objects:
            with open(os.path.join(self.path,'study.p'),'rb') as f:
                study_obj = pickle.load(f)
                self.__dict__ = study_obj.__dict__
        if load_data:
            self.output_collector.load_data(json.load(open(os.path.join(self.path,'data.json'),'rb')))

    def _run(self):
        raise NotImplementedError