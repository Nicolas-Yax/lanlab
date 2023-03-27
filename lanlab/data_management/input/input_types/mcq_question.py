from lanlab.data_managing.input.question import Question

class MCQuestion(Question):
    def __init__(self,q=None):
        if q is None:
            q = {'prompt':None,'options':[],'keywords':None,'info':None}
        self.load(q)
    def load(self,q):
        super().load(q)
        self.options = q['options']
    def setup(self,config):
        self.answer_format = config['answer_format']
        self.extraction_format = config['extraction_format']
    def _write_options_part(self):
        s = ''
        for i in range(len(self.options)):
            s_answer = str(self.mcq_format)
            s_answer = s_answer.replace('[letter]',chr(97+i))
            s_answer = s_answer.replace('[number]',str(i+1))
            s_answer = s_answer.replace('[answer]',self.options[i])
            s += s_answer
        return s
    def _write_extraction_part(self):
        return self.extraction_format
    def __str__(self):
        s = self._write_question_part()
        s += self._write_options_part()
        s += '\n'
        s += self._write_answer_part()
        s += self._write_extraction()
        return s