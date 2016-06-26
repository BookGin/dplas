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

if len(sys.argv) != 3:
    print("Usage: ./build.py inputfile inverted-file-suffix")
    sys.exit(0)

vocabs = []
doc_freqs = []
TOTAL_DOCS = []
AVG_DOC_LENS = []

total_load_file = 0
while total_load_file >= 0:
    path = "%s/%d" % (sys.argv[2], total_load_file)
    try:
        vocabs.append(json.load(open( "%s.vocab" % path, 'r')))
        doc_freqs.append(json.load(open("%s.freq" % path, 'r')))
        misc = json.load(open("%s.misc" % path, 'r'))
        TOTAL_DOCS.append(misc["total_doc"])
        AVG_DOC_LENS.append(misc["avg_len"])
        total_load_file += 1
    except FileNotFoundError:
        print("%d.{vocab, freq, misc} not found" % total_load_file)
        print("Loaded %d inverted files." % total_load_file)
        break


def getTF(term, doc, topic_index):
    raw_tf = doc.count(term)
    return (raw_tf * (OKAPI_K + 1)) / (raw_tf + OKAPI_K * (1 - OKAPI_B + OKAPI_B * len(doc) / AVG_DOC_LENS[topic_index]))

def getIDF(term, topic_index):
    return math.log((TOTAL_DOCS[topic_index] - doc_freqs[topic_index][term] + 0.5) / (doc_freqs[topic_index][term] + 0.5))

def getTFIDF(term, doc, topic_index):
    return getTF(term, doc, topic_index) * getIDF(term, topic_index)

def segment(string):
    return jieba.cut_for_search(string)

def getVector(qry, topic_index):
    vec = []
    for term in vocabs[topic_index].keys():
        vec.append(getTFIDF(term, qry, topic_index))
    return Np.array(vec)



with open(sys.argv[1], "r") as f:
    qry = ""
    for line in f.readlines():
        qry += line

for topic_index in range(total_load_file):
    qry_vec = getVector(qry, topic_index)
    print("%d norm = %f" % (topic_index, Np.linalg.norm(qry_vec)))
#print(Np.dot(qry_vec, qry2_vec) / (Np.linalg.norm(qry_vec) * Np.linalg.norm(qry2_vec)))
