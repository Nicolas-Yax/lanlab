```python
import os
import logging

from lanlab.models.openai_models import *
from lanlab.studies.one_model import *
from lanlab.data_management.input.input_collector.question_dataset import QuestionDataset
from lanlab.data_management.input.input_types.question import Question
```

# Language Lab Framework

The point of this framework is to simplify the black box studies with LLMs by providing query tools to automate the interactions with the model as well as to provide tools to analyse very simply the data from these interactions

This presentation should give you a quick overview about what you can do with this framework as well as more advanced ways to use it if you want to go further.

This framework tries to implement new programmation paradygmes such as :
- time capsule (load any study at any time in the version of the framework it ran originaly without any effort)
- automatic saving, naming and sorting (don't bother about saving your work everything is saved automatically and sorted accordingly)
- Data collection and analyses in the same script (you don't need to split your script in data collection / data analysis anymore - data saving and loading is done with the same function run : the framework will automatically run the study if it hasn't done it before else it will load the data)

# SETUP

- Install the libraries (developped in Python 3.7.3 but any Python3 should be enough) with requirements.txt
- Put your openAI access token in lanlab/models/_env -> OPENAI_API_KEY (copy paste it from the website) and then rename _env in .env

# Easy use

## Building the Dataset for the study


```python
#Define your dataset
dataset = QuestionDataset()
input_data_path = os.path.join('inputs','questionnaire.json') #Path to the input data
input_data_format = Question #Format of the input data
dataset.from_json(input_data_path,input_data_format) #Loading the data with the given format
```

When loading input data as Questions, the question format has been automatically loaded. It can be accessed and modified through the config attribute :


```python
dataset.questions[0].config
```




    {'format': 'Q:[prompt]\nA:'}



The default format makes questions like :
```
Q:[Question]
A:
```


```python
for i,q in enumerate(dataset):
    print('--- Question',i)
    print(q)
```

    --- Question 0
    Q:What is 2+2 ?
    A:
    --- Question 1
    Q:What is the Capital of France ?
    A:
    --- Question 2
    Q:What is the air speed velocity of an unladen swallow ?
    A:
    --- Question 3
    Q:Here is a list of 16 numbers. What is the next one ?
    7
    4
    3
    7
    4
    3
    7
    4
    3
    7
    4
    3
    7
    4
    3
    
    A:



```python
dataset['format'] = 'Question:[prompt]\nAnswer:'
```

With this new format we get
```
Question:[Question]
Answer:
```


```python
for i,q in enumerate(dataset.questions):
    print('--- Question',i)
    print(q)
```

    --- Question 0
    Question:What is 2+2 ?
    Answer:
    --- Question 1
    Question:What is the Capital of France ?
    Answer:
    --- Question 2
    Question:What is the air speed velocity of an unladen swallow ?
    Answer:
    --- Question 3
    Question:Here is a list of 16 numbers. What is the next one ?
    7
    4
    3
    7
    4
    3
    7
    4
    3
    7
    4
    3
    7
    4
    3
    
    Answer:


## Choosing the Model

Now that we have a question dataset we also need to choose the LLM we will be working with. Many models are availabel in the framework and more will be to come ! Let's focus on the OPENAI models for now :


```python
#List of openai models available
get_openai_model_classes()
```




    [lanlab.models.openai_models.AD,
     lanlab.models.openai_models.AD1,
     lanlab.models.openai_models.BB,
     lanlab.models.openai_models.BB1,
     lanlab.models.openai_models.CU,
     lanlab.models.openai_models.CU1,
     lanlab.models.openai_models.DV,
     lanlab.models.openai_models.DVB,
     lanlab.models.openai_models.DV1,
     lanlab.models.openai_models.CDV2,
     lanlab.models.openai_models.DV2,
     lanlab.models.openai_models.DV3]




```python
#Load an interface to text-davinci-003
model = DV3()
```

The model also has a default configuration you can update :


```python
print(model.config)
```

    {'temperature': 1.0, 'max_tokens': 16, 'top_p': 1, 'stop': None, 'logit_bias': {}}


Let's set the temperature to 0.7 and increase the number of tokens to be generated


```python
model.config['max_tokens'] = 256
model.config['temperature'] = 0.7
print(model.config)
```

    {'temperature': 0.7, 'max_tokens': 256, 'top_p': 1, 'stop': None, 'logit_bias': {}}


## Selecting the study to run

It's almost finished. Now we only need to select what to do with this dataset and these models.

For this example we'll run a very simple study that iterates n times each question in the dataset for a single model. A class is already provided with this procedure. You are free to define your own studies if you want to do more specific things. It's very easy ! (see the Define your own studies section)


```python
#Choose the type of study you want to run and plug the dataset and the model in
study = OneModelStudy(dataset,model,name='test') #Naming the study is also important

#We can finally configure the study
study['prepend'] = 'You are a language model answering questions.\n' #Context before asking the question
#Start the answer by
study['append'] = ' The answer is'
#Number of answer you want for each question
study['nb_run_per_question'] = 5
```

With this setup the final prompt sent to the language model will be
```
You are a language model answering questions.
Question:[Question]
Answer: The answer is
```

Note that "format" in the configuration dataset is redundant with the study configuration "prepend" and "append". Indeed you could put the prepend and the append in the format but it can become messy very quickly. Prepend and Append are essentially for convenience : in the dataset you explain how to format questions and in the study you add the context and you can prompt the answers.

Now we can run the study


```python
#Run it and automatically save the results. 
#If it has already been run it will automatically load the results
study.run()
```

That's it we have the results ! Here we defined each part (dataset, model, and study) by hand but you can define your own classes to avoid having to do it everytime (see the Define your own studies part).

# Analyses

From an existing study you can run analyses to quantify what you are interested in in these studies. Here is an example of two analyses that are already implemented : Accuracy checking and LogScores to know if the model knows the input text.

## Accuracy

The accuracy metrics is tries to correct Question items automatically by using the keywords item. It simply checks whether one of the keywords associated with the "correct" label is found in the completion. If it is the completion is considered as a correct answer. If it's not it's considered as wrong.


```python
import matplotlib.pyplot as plt

from lanlab.analyses.accuracy.accuracy_analysis import AccuracyAnalysis

#Load the analysis
accuracy_analysis = AccuracyAnalysis(study)
```

Output data matrix : question_index x 2 (correct / wrong)


```python
accuracy_analysis.data
```




    array([[5., 0.],
           [5., 0.],
           [0., 5.],
           [3., 2.]])



Plot of the matrix


```python
accuracy_analysis.plot()
plt.legend()
plt.show()
```


    
![png](main_files/main_39_0.png)
    


## Logscores

The logscore analysis is a tool that tries to quantify how much the model knows a text by heart. This can be particularly useful when doing questionnaires with language models as some questions might already be in the training corpus. With this method we can score how much the model has already seen the question (and thus maybe the answer to this question).

To do this we compute the logprobability of the sequence up to token t and plot it. If the model is very confident about its prediction the logprobability of the new tokens should be 0 (probability of 1) and therefore it will result in an horizontal graph on the areas the model knows the text.

We can thus visualize the graph (called loggraph) and also quantify how much horizontal the graph is by fitting a model on it such as :
$f(x) = A(1-exp(-Bx))$ and plot the parameters A and B.

In the previous study we used a prepend and a specific formatting. Here we are only interested in the text of the question and we don't want to add framing around it. A study subclassing the OneModelStudy with all the required configuration has already been defined setting all the required parameters.

Moreover for the example I have chosen specific texts to show the concept behind the logscores and their limitations.


```python
from lanlab.studies.collect_logprobs import CollectLogProbsStudy

ls_dataset = QuestionDataset()
ls_dataset.from_json(os.path.join('inputs','books.json'),Question)

ls_study = CollectLogProbsStudy(ls_dataset,model,name='logscores')

ls_study.run()
```

Now let's run the analysis


```python
from lanlab.analyses.logscore.logscore_analysis import LogScoreAnalysis
import matplotlib.pyplot as plt

#Create the analysis object
logscore_analysis = LogScoreAnalysis(ls_study)
```

We can now visualize the logpgraphs


```python
logscore_analysis.plot_index(0)
```


    
![png](main_files/main_48_0.png)
    


This is the loggraph for the first text. As you see it is very horizontal because it's an excerpt from The Lord of the Ring by J.R.R Tolkien. It's a very famous text and the model doesn't hesitate very much to complete it. The small bumps often come from punctuation as the model doesn't know at the beginning of the completion whether it should input a newline for every sentence or continue on the same line after the dot.

Here are all the loggraphs :


```python
plt.figure(figsize=(10,10))
for i in range(4):
    ax = plt.subplot(2,2,i+1)
    logscore_analysis.plot_index(i)
    ax.set_title(str(i))
plt.tight_layout()
plt.legend()
plt.show()
```


    
![png](main_files/main_51_0.png)
    


We clearly see that in all of the texts 0, 1 and 2 the model doesn't hesitate that much than in the text number 4. Indeed The first 2 are taken from famous books, the 3rd one has patterns than can easily be predicted and the 4th one is a random text taken on a forum on the internet.


```python
for i,q in enumerate(ls_dataset):
    print('--- Text',i)
    print(q)
```

    --- Text 0
    In a hole in the ground there lived a hobbit.
    
    Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort.
    --- Text 1
    So long as there shall exist, by virtue of law and custom, decrees of damnation pronounced by society, artificially creating hells amid the civilization of earth, and adding the element of human fate to divine destiny; so long as the three great problems of the century—the degradation of man through pauperism, the corruption of woman through hunger, the crippling of children through lack of opportunity—are unsolved; so long as social asphyxia is possible in any part of the world;—in other words, and with a still wider significance, so long as ignorance and poverty exist on earth, books of the nature of Les Misérables cannot fail to be of use.
    --- Text 2
    The A is better than the B.
    The B is better than the C.
    The C is better than the D.
    The D is better than the E.
    The E is better than the F.
    The F is better than the G.
    The G is better than the H.
    The H is better than the I.
    The I is better than the J.
    The J is better than the K.
    --- Text 3
    You need to escape the \ in your string (turning it into a double-\), otherwise it will become a newline in the JSON source, not the JSON data.


There are 2 ways to produce an horizontal line : either the model knows perfectly the text or it can infer it from the context. This method is unable to differentiate the two. Even in the latter scenario shouldn't be as strong as the first one (like we can see in the 3rd loggraph the logprobs don't saturate as quickly as in the first two texts), we can find example where it saturates much quicker.

Therefore this method can be used to know if the model already knows the given text or if it can infer the rest of the text from its beginning. If one could ensure that the rest of the text cannot be guessed from the beginning (by avoiding asking questions such as completing the sequence 123123123123) we get a tool that measures how much the model knows the input text.

Plot the parameters of the fitted models :


```python
logscore_analysis.plot_comparison()
plt.legend()
plt.show()
```


    
![png](main_files/main_56_0.png)
    


We get one cluster with 0 1 and 2 and 3 is much farther. Empirically, if the value of A is around or less than $10^0$ and B is more than or close to $10^0$, there is a probable contamination.

Let's go back to our initial questionnaire.


```python
from lanlab.studies.collect_logprobs import CollectLogProbsStudy

ls_dataset = QuestionDataset()
ls_dataset.from_json(os.path.join('inputs','questionnaire.json'),Question)

ls_study = CollectLogProbsStudy(ls_dataset,model,name='logscores')

ls_study.run(update_objects=True)

#Create the analysis object
logscore_analysis = LogScoreAnalysis(ls_study)
```


```python
logscore_analysis.plot_comparison()
plt.legend()
plt.show()
```


    
![png](main_files/main_60_0.png)
    


We see probable contamination in 2 and 3 as they are close to 10^0 (careful it's a log scale - question 0 is quite far from 10^0). Let's see the loggraphs


```python
plt.figure(figsize=(10,10))
for i in range(4):
    ax = plt.subplot(2,2,i+1)
    logscore_analysis.plot_index(i)
    ax.set_title(str(i))
plt.tight_layout()
plt.legend()
plt.show()
```


    
![png](main_files/main_62_0.png)
    


2 might be contaminated and indeed it's a famous quote so the model recognizes it (except the "?" at the end which surprises it very much). 3 is a case of in context learning as we can see it in the question.


```python
for i,q in enumerate(ls_dataset):
    print('--- Text',i)
    print(q)
```

    --- Text 0
    What is 2+2 ?
    --- Text 1
    What is the Capital of France ?
    --- Text 2
    What is the air speed velocity of an unladen swallow ?
    --- Text 3
    Here is a list of 16 numbers. What is the next one ?
    7
    4
    3
    7
    4
    3
    7
    4
    3
    7
    4
    3
    7
    4
    3
    


# Saving and Time Capsule

In this framework when you run 
```python
study.run()
```
the results are stored in 2 files :
- data.json which contains the output data as well as some of the input data
- study.p which is a pickle version of the study object.

These files are stored in a path relative to the content of the training (names or study, dataset and model to be more precise).
If another study is run with the same pathing instead of running it will load the study.p file with the data in data.json. This is the concept the framework is based on for 
- Saving and Loading data accordingly (if you build a study with the same path as another that has already run) it means you are running the same study as the one before and the framework shouldn't compute the same data twice : it loads the previous one.
- Time capsule : it saves the environment in which you ran each experiment. Therefore you can load the exact environment even 10 years later to replicate old results when needed even if the framework has changed in between.

When creating a Study object and running it so that it loads a previous study it will drop the study object you built to load the study.p . If you want to update the study.p file you can use the ```python study.run(update_objects=True)``` parameter to keep the version of study you built and erase the study.p file to replace it with the study built.

If you don't want to load the data and recompute it you can use ```python study.run(update_data=True)```.

The default value of these parameters is False and both can be used together.


```python
study.run(update_objects=True,update_data=True)
```

    100%



```python
accuracy_analysis2 = AccuracyAnalysis(study)

print('First run (data are now discarded from the data.json file)')
accuracy_analysis.plot()
plt.show()

print('Second run (new data in the data.json file)')
accuracy_analysis2.plot()
plt.show()
```


    
![png](main_files/main_68_0.png)
    



    
![png](main_files/main_68_1.png)
    

