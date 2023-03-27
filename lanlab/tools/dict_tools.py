import logging
import copy

def to_dict(d):
    if isinstance(d,list):
        for i in range(len(d)):
            d[i] = to_dict(d[i])
    elif isinstance(d,dict):
        for k in d:
            d[k] = to_dict(d[k])
    elif isinstance(d,SafeDict):
        return d.to_dict()
    return d

class SafeDict:
    """ Dictionary for which an error is returned if the user tries to assign an unknown variable (useful to be sure that there aren't spelling mistakes in the config parameters) """
    def __init__(self,d=None):
        if d is None:
            d = {}
        self.d = d
    def load_from(self,d):
        if not(d is None):
            for k in d:
                self[k] = d[k]
    def __getitem__(self,k):
        return self.d[k]
    def __setitem__(self,k,v):
        try:
            self.d[k]
            self.d[k] = v
        except KeyError:
            logging.error('Key '+k+" not in SafeDict "+str(self.__class__)+" with keys "+str(list(self.keys())))
            raise KeyError #"Key not in SafeDict"

    def __iter__(self):
        return iter(self.d)

    def set(self,k,v):
        self.d[k] = v

    def copy(self):
        return SafeDict(self.d.copy())

    def to_dict(self):
        return self.d
    
    def __str__(self):
        return str(self.d)
    
    def __repr__(self):
        return str(self)

    def __eq__(self,o):
        return self.d == o.d