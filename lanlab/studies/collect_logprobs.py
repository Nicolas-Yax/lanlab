from lanlab.studies.one_model import OneModelStudy

class CollectLogProbsStudy(OneModelStudy):
    def __init__(self,input_collector,model,name=None,reconfigure_model=True,reconfigure_input_collector=True):
        #Reconfigure the input_collector to be minimal
        if reconfigure_input_collector:
            input_collector['format'] = '[prompt]'
        #Reconfigure the model to be minimal
        if reconfigure_model:
            model['max_tokens'] = 1
        #Minimal OneModelStudy config
        super().__init__(input_collector,model,name=name)
        self['append'] = ''
        self['prepend'] = ''
        self['nb_run_per_question'] = 1