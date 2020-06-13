#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 18:22:25 2020

@author: pushkara
"""


import json
import requests

url='http://127.0.0.1:5000/api/'
text = "how are you"
data = json.dumps({'s1':text})
r = requests.post(url,data).json()
print(r.values())
