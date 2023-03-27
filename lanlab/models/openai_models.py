import openai
import time
from decouple import config
import logging

from lanlab.models.model import OnlineModel
from lanlab.tools.dict_tools import SafeDict
from lanlab.data_management.output.output_types.completion import Completion

openai.api_key = config('OPENAI_API_KEY')

class UnsplittableQuery(Exception):
    def __init__(self):
        super().__init__()
        self.message = "The query cannot be found in the token list. This could either be due to a bug so that the query and the list of tokens mismatch or it could be due to a retokenization issue (if A is a list of token : tokenize(detokenize(A)) != A)."

def split_token_list(l,query):
    s = ""
    if s == query:
        return l
    for i in range(len(l)):
        s += l[i]
        if s == query:
            return l[:i+1],l[i+1:]
    raise UnsplittableQuery

def completion_from_OPENAI(d,query):
    completion = Completion()
    completion["model"] = d['model']
    input_tokens,output_tokens = split_token_list(d['choices'][0]['logprobs']['tokens'],query)
    completion["tokens"] = {'prompt':input_tokens,'completion':output_tokens}
    completion["logp"] = {'prompt':d['choices'][0]['logprobs']['token_logprobs'][:len(input_tokens)],
        'completion':d['choices'][0]['logprobs']['token_logprobs'][len(input_tokens):]}
    completion["top_logp"] = {'prompt':[dict(e) if not(e is None) else None for e in d['choices'][0]['logprobs']['top_logprobs'][:len(input_tokens)]],
        'completion':[dict(e) if not(e is None) else None for e in d['choices'][0]['logprobs']['top_logprobs'][len(input_tokens):]]}
    completion["finish_reason"] = d['choices'][0]["finish_reason"]
    return completion

class GPT(OnlineModel):
    def __init__(self):
        super().__init__()
        self.config = SafeDict()
        self.config.d['temperature'] = 1.
        self.config.d['max_tokens'] = 16
        self.config.d['top_p'] = 1
        self.config.d['stop'] = None
        self.config.d['logit_bias'] = {}

    @property
    def name(self):
        raise NotImplementedError

    @property
    def engine(self):
        return NotImplementedError

    def ask(self,input_config):
        #valid = self.valid(input_config,openai.Completion.create)
        #if not valid:
        #    raise ValueError #The given parameters aren't valid

        try:
            answer = openai.Completion.create(
                **input_config.to_dict(),
                engine=self.engine,
                logprobs=5,
                echo=True)
            #Extract the text from the answer
            out_text = answer.get('choices')[0].get('text')
            return completion_from_OPENAI(answer,input_config['prompt'])
        except openai.error.APIError: #Due to the internet network errors may occur and a new request can be sent
            logging.log('[openai API Error] : Retrying in 1 sec')
            self.error_count += 1
            if self.error_count > self.error_count_max:
                logging.error('Too many errors : the process will stop')
                assert False #Too many errors in communicating with the server -> The process will stop to avoid spending too much money in bugs
            time.sleep(1) #Wait 1 sec before sending another request
            return self.ask(input_config)
        #except openai.error.ServiceUnavailableError: #This error seems to have been removed from the API
        #    time.sleep(10)
        #    return self.ask(prompt)
        except openai.error.RateLimitError: #Triggered when interacting with models with limitation rates (such as code-davinci-002 that only accepts 20 requests / min)
            logging.info('[openai RateLimitError] : Retrying in 1 min')
            time.sleep(62)
            return self.ask(input_config)

class AD(GPT):
    @property
    def engine(self):
        return 'ada'
    @property
    def name(self):
        return 'AD'

class AD1(GPT):
    @property
    def engine(self):
        return 'text-ada-001'
    @property
    def name(self):
        return 'AD1'

class BB(GPT):
    @property
    def engine(self):
        return 'babbage'
    @property
    def name(self):
        return 'BB'

class BB1(GPT):
    @property
    def engine(self):
        return 'text-babbage-001'
    @property
    def name(self):
        return 'BB1'

class CU(GPT):
    @property
    def engine(self):
        return 'curie'
    @property
    def name(self):
        return 'CU'

class CU1(GPT):
    @property
    def engine(self):
        return 'text-curie-001'
    @property
    def name(self):
        return 'CU1'

class DV(GPT):
    @property
    def engine(self):
        return 'davinci'
    @property
    def name(self):
        return 'DV'

class DVB(GPT):
    @property
    def engine(self):
        return 'davinci-instruct-beta'
    @property
    def name(self):
        return 'DVB'

class DV1(GPT):
    @property
    def engine(self):
        return 'text-davinci-001'
    @property
    def name(self):
        return 'DV1'

class CDV2(GPT):
    @property
    def engine(self):
        return 'code-davinci-002'
    @property
    def name(self):
        return 'CDV2'

class DV2(GPT):
    @property
    def engine(self):
        return 'text-davinci-002'
    @property
    def name(self):
        return 'DV2'

class DV3(GPT):
    @property
    def engine(self):
        return 'text-davinci-003'
    @property
    def name(self):
        return 'DV3'

def get_openai_model_classes():
    return [AD,AD1,BB,BB1,CU,CU1,DV,DVB,DV1,CDV2,DV2,DV3]