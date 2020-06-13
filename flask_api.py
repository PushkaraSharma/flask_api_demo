#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 18:02:16 2020

@author: pushkara
"""
from flask import Flask,jsonify,request,abort
import _pickle as pickle
from nltk.corpus import stopwords
import string
from nltk import word_tokenize


app = Flask(__name__)

def bag_words(words):
        stop_words = stopwords.words('english')
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



@app.route('/api/',methods=['POST'])

def predict():
    data = request.get_json(force=True)
    predict_req  = [data['s1']]
    print(predict_req[0])
    prediction = classifier.classify(bag_words(predict_req[0]))
    if  prediction ==0:
        prediction = 'Ham'
    else:
        prediction = 'Spam'
    return jsonify(results = prediction)

if __name__ == "__main__":
    classifier = pickle.load(open("ham_spam.pkl","rb"))
   
    
    
    app.run(debug=True)
