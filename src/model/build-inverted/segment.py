#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import sys
import jieba
import json
jieba.set_dictionary('../../../dict.txt.big')

# Segment docs per line with space
# Usage: ./genInverted.py input output

docs = []
# one doc per line
with open(sys.argv[1], "r") as f:
    for doc in f.readlines():
        docs.append(jieba.cut_for_search(doc))

for doc in docs:
    for term in doc:
        print(term, end = " ")
    print()

