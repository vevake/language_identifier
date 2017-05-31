import re
import numpy as np
import math
import pandas as pd
import  sys
import os

#variable use to store the traindata information
labels = [] #list of all possible output labels 
word_count = {} #number of times a word is seen during training
label_word_count = [] #number of time a word is seen for a particular label
documents = {} #number of documents seen for a label while training

def tokenize(text):
    '''
    Used to tokenize the words in a statement 
    '''
    text = text.lower()
    text = re.sub('/\W/g', ' ', text)
    text = re.sub('/\s+/g', ' ', text)
    text = text.split();
    return text

def train(text, label):
    '''
    trains the model given a text and its label (i.e) computes the word counts on the training data
    '''
    if label not in labels:
        labels.append(label)
        label_word_count.append({})
        documents[label] = 0
    words = tokenize(text)
    length = len(words)
    for i in range(len(words)):
        s = words.pop()
        try:
            word_count[s] += 1
        except:
            word_count[s] = 1    
        try :
            label_word_count[labels.index(label)][s] += 1    
        except:
            label_word_count[labels.index(label)][s] = 1    
    documents[label] += 1

def inverseWordLabelCount(word, label):
    '''
    returns the number of times a word was seen in other labels.
    '''
    count = 0
    for i in range(len(labels)):
        if labels[i]!= label:
            try :
                count += label_word_count[i][word]
            except:
                count += 0
    return count

def get_wordCountforLabel(word, label):
    '''
    returns the number of times a word was seen for a given label
    '''
    try:
        count = label_word_count[labels.index(label)][word]
    except:
        count = 0
    return count

def predict(text):
    '''
    predicts the language of the given text using Bayes theorem.
    '''
    scores={} #saves the scores for the predictions
    for i in range(len(labels)):
        label = labels[i]
        d = documents[label]
        total_count = sum(documents.values())
        inverse_count = total_count - d
    l = len(labels) 
    probability = np.zeros(l)
    for i in range(len(labels)):
        label = labels[i]
        logSum = 0 
        probability[i] = float(d) / float(total_count)
    
        words = tokenize(text)
        for j in range(len(words)):
            word = words[j]
            try:
                _word_count = word_count[word]
            except:
                _word_count = 0
            if _word_count == 0 :
                continue
            else:
                wordProbability = float(get_wordCountforLabel(word,label)) / documents[label]                
                wordInverseProbability = float(inverseWordLabelCount(word, label))/float(inverse_count)
                bayes_prob = wordProbability / (wordProbability + wordInverseProbability) #Bayes rule

                if (bayes_prob == 0):
                    bayes_prob = 0.01
                elif (bayes_prob == 1):
                    bayes_prob = 0.99
            logSum += (math.log(1 - bayes_prob) - math.log(bayes_prob));
        scores[label] = 1 / ( 1 + math.exp(logSum) );
    pred = max(scores, key=scores.get)
    pred_prob = scores[pred]
    return pred, pred_prob

def test(file_path = 'test_data.csv'):
    '''
    test the trained model on DLI32 dataset
    '''
    print 'Testing on DLI32 dataset...'
    test_data = pd.read_csv(file_path)
    count = 0
    for i in range(len(test_data)):
        orig_label = test_data['language'][i]
        pred_label, pred_prob = predict(test_data['text'][i])
        # print pred_label, pred_prob
        if orig_label == pred_label:
            count += 1
    print 'Accuracy :', float(count)/float(len(test_data))

if __name__ == '__main__':
    test_mode = 'auto'
    if len(sys.argv) == 2:
       test_file = sys.argv[1]
       if os.path.exists(test_file) :
           test_mode = 'file'
       else:
           test_mode = 'sentence'
    else:
        test_string = None

    #train data
    data = pd.read_csv('train_data.csv')
    # print 'Started Training model on DLI32-2 dataset with 32 languages...'
    for i in range(len(data)):
        train(data['text'][i], data['language'][i])
    #print 'Training Completed'
    
    #testing
    if test_mode == 'sentence':
        print '1'
        pred_label, pred_prob = predict(test_file)
        print pred_label, pred_prob 
    elif test_mode =='file':
        print '2'
        test(file_path=test_file)
    else:
        print '3'
        test()