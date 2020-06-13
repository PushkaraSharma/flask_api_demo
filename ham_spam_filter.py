import pandas as pd
from nltk.corpus import stopwords
import string
#from nltk.stem import PorterStemmer
from nltk import word_tokenize
from sklearn.preprocessing import LabelEncoder
from nltk import NaiveBayesClassifier
from nltk import classify
import _pickle as pickle


def train_model():
    df = pd.read_csv('spam.csv',encoding = 'latin-1')
    Y = df['v1']
    X = df['v2']
    lb = LabelEncoder()
    Y = lb.fit_transform(Y)

    global stop_words
    stop_words = stopwords.words('english')
    #ps = PorterStemmer()

    final = []
    for i in range(len(Y)):
        final.append((bag_words(X[i]),Y[i]))

    from sklearn.model_selection import train_test_split
    training,testing = train_test_split(final,test_size = 0.25)


    classifier = NaiveBayesClassifier.train(training)
    acc = classify.accuracy(classifier,testing)

    pickle.dump(classifier,open("ham_spam.pkl","wb"))
    return acc,classifier



def bag_words(words):
    processed = words.lower()
    processed = processed.replace(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', 'email')
    processed = processed.replace(r'^\D?(\d{3})\D?\D?(\d{3})\D?(\d{4})$', 'phoneno')
    processed = processed.replace(
        r'^(http(s?)\:\/\/)*[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?$',
        'website')
    processed = processed.replace(r'$|\£|\€', 'money')
    processed = processed.replace(r'\d+(\.\d+)?', 'number')
    processed = processed.replace(r'^\s+|\s+?$', '')
    processed = processed.replace(r'\s+', ' ')

    words = word_tokenize(processed)
    clean = []
    for i in words:
        if i not in stop_words or i not in string.punctuation:
            clean.append(i)
    dicton = dict([word, True] for word in clean)
    return dicton

acc,classifier = train_model()


def testing(input):

    #testing_strings = ['You won the lottery of $2000','meet me soon','log in to facebook today']

    #pred = []
    #for i in testing_strings:
    #    pred.append(classifier.classify(bag_words(i)))
    #pred
    prediction = classifier.classify(bag_words(input))
    if  prediction ==0:
        print('Ham')
    else:
        print('Spam')
train_model()
testing('call me as soon as possible')