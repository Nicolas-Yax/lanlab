import pickle
import os
import json

class OutputCollector:
    def __init__(self):
        self.data = [] #The data should all be put here else you'll have to overload the save method to save it
    
    def add(self,key,input,output):
        raise NotImplemented

    def pop_data(self):
        d = self.data
        self.data = []
        return d

    def set_data(self,d):
        self.data = d

    def save_data(self,study):
        with open(os.path.join(study.path,"data.json"),'w') as f:
            json.dump(self.dump_data(),f)

    def save(self,study):
        #Save the data on one side
        self.save_data(study)
        #Save the object empty of data on the other side
        (data,self.data) = (self.data,{})
        with open(os.path.join(study.path,'output_collector.p'),'wb') as f:
            pickle.dump(self,f)
        self.data = data