from lanlab.data_management.input.input_types.input_type import InputType

class Text(InputType):
    def __init__(self,t):
        self.t = t

    def __str__(self):
        return self.t

    def config_class(self):
        return dict