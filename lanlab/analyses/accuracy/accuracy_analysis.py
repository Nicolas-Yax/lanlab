import numpy as np
import matplotlib.pyplot as plt

from lanlab.analyses.analysis import Analysis

class AccuracyAnalysis(Analysis):
    def __init__(self,study,*args,**kwargs):
        self.data = np.zeros((len(study.input_collector),2))

        super().__init__(study,*args,**kwargs)

    def run(self,study):

        for i,q in enumerate(study.input_collector):
            for j in range(len(study.output_collector.data[i])):
                tokens = study.output_collector.data[i][j]['output']['tokens']['completion']
                out_text = ""
                for t in tokens:
                    out_text += t
                incorrect = True
                for k in range(len(q.keywords['correct'])):
                    if q.keywords['correct'][k] in out_text:
                        incorrect = False
                        break
                if incorrect:
                    self.data[i][1] += 1
                else:
                    self.data[i][0] += 1

    def plot(self):
        plt.bar(range(len(self.data)),self.data[:,0],color='green',label='correct')
        plt.bar(range(len(self.data)),self.data[:,1],bottom=self.data[:,0],color='red',label='wrong')
        plt.xticks(range(len(self.data)))
        plt.xlabel('Question index')
        plt.ylabel('Proportions of answers')