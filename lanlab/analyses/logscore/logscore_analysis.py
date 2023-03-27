import matplotlib.pyplot as plt
import numpy as np

from lanlab.analyses.analysis import Analysis
from lanlab.analyses.logscore.logscore_model import ExponentialModel

def init_sequence(seq):
    """ Replace the first logprob by 0 """
    return np.concatenate([[0],np.array(seq[1:])])


def plot_loggraph(logprobs,tokens=None,normalize=False):
    """ Plot the loggraph of the sequence """
    #Set the first token prob to 0
    _logprobs = init_sequence(logprobs)
    #Set x and y for plotting
    x = np.array(range(len(_logprobs)))
    y = np.cumsum(logprobs)
    if normalize:
        x = x/len(x)
        y = y/len(x)
    #Plotting
    plt.plot(x,y)
    #Legends
    plt.gca().set_xticks(x)
    plt.xlabel('Token indexs')
    if not(tokens is None):
        plt.gca().set_xticklabels(tokens,rotation=90)
        plt.xlabel('Tokens')
    plt.ylabel('Cumulative logprobability')

class LogScoreAnalysis(Analysis):
    def __init__(self,*args,model_class=ExponentialModel,**kwargs):
        self.model_class = model_class
        self.data = []

        super().__init__(*args,**kwargs)

    def run(self,study):
        for i,q in enumerate(study.input_collector): #Iterate over questions
            tokens = study.output_collector.data[i][0]['output']['tokens']['prompt']
            logprobs = init_sequence(study.output_collector.data[i][0]['output']['logp']['prompt'])
            model = self.model_class()
            x = np.array(range(len(logprobs)))/len(logprobs)
            y = np.cumsum(logprobs)/len(logprobs)
            model.fit(x,y)
            self.data.append((tokens,logprobs,model))

    def plot_comparison(self):
        fig = plt.figure()
        for i,(t,lp,m) in enumerate(self.data):
            plt.scatter([m.params[0]],[m.params[1]],label=str(i))
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('A')
        plt.ylabel('B')

    def plot_index(self,i):
        tokens,logprobs,m = self.data[i]
        plot_loggraph(logprobs,tokens=tokens,normalize=True)
        x = np.array(range(len(tokens)))
        xn = x/len(x)
        y = m(xn)
        plt.plot(xn,y,label="model")