#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math
import json
import sys
import numpy as Np
import jieba
jieba.set_dictionary('../dict.txt.big')


OKAPI_K = 1.6
OKAPI_B = 0.75

vocab = json.load(open( "%s.vocab" % sys.argv[1], 'r'))
doc_freq = json.load(open("%s.freq" % sys.argv[1], 'r'))
misc = json.load(open("%s.misc" % sys.argv[1], 'r'))
TOTAL_DOC = misc["total_doc"]
AVG_DOC_LEN = misc["avg_len"]

def getTF(term, doc):
    raw_tf = doc.count(term)
    return (raw_tf * (OKAPI_K + 1)) / (raw_tf + OKAPI_K * (1 - OKAPI_B + OKAPI_B * len(doc) / AVG_DOC_LEN))

def getIDF(term):
    return math.log((TOTAL_DOC - doc_freq[term] + 0.5) / (doc_freq[term] + 0.5))

def getTFIDF(term, doc):
    return getTF(term, doc) * getIDF(term)

def segment(string):
    li = []
    for i in jieba.cut_for_search(string):
        li.append(i)
    return li

def getVector(qry):
    vec = []
    for term in vocab.keys():
        vec.append(getTFIDF(term, qry))
    return Np.array(vec)

# MAIN
with open(sys.argv[1], "r") as f:
    qry = ""
    for line in f.readlines():
        qry += line

qry_vec = getVector(qry)
for i in qry_vec:
    print(i, end=" ")
