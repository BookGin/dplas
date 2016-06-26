#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math
import sys
import jieba
import json
jieba.set_dictionary('../dict.txt.big')


# Usage: ./genInverted.py inputdocs [doc_freq] [vocab] [misc]

docs = []
doc_freq = {}
vocab = {}
total_doc_len = 0

def segment(string):
    li = []
    for i in jieba.cut_for_search(string):
        li.append(i)
    return li

# one doc per line
with open(sys.argv[1], "r") as f:
    for doc in f.readlines():
        docs.append(segment(doc))

for doc in docs:
    total_doc_len += len(doc)
    for term in doc:
        if term in vocab:
            vocab[term] += 1
        else:
            vocab[term] = 1

for term in vocab:
    count = 0
    for doc in docs:
        count += 1 if term in doc else 0
    doc_freq[term] = count

print("Finished building.")
if (len(sys.argv) > 2):
    with open(sys.argv[2], "w") as f:
        f.write(json.dumps(doc_freq, ensure_ascii=False))
    with open(sys.argv[3], "w") as f:
        f.write(json.dumps(vocab, ensure_ascii=False))
    with open(sys.argv[4], "w") as f:
        js = {}
        js["total_doc"] = len(docs)
        js["total_len"] = total_doc_len
        js["avg_len"] = total_doc_len / len(docs)
        f.write(json.dumps(js, ensure_ascii=False))
else:
    print("Dump doc freq to:")
    output_doc_freq = input()
    with open(output_doc_freq, "w") as f:
        f.write(json.dumps(doc_freq, ensure_ascii=False))
    print("Dump vocabulary to:")
    output_vocab = input()
    with open(output_vocab, "w") as f:
        f.write(json.dumps(vocab, ensure_ascii=False))
    print("Dump misc info to:")
    output_doc_freq = input()
    with open(output_doc_freq, "w") as f:
        js = {}
        js["total_doc"] = len(docs)
        js["total_len"] = total_doc_len
        js["avg_len"] = total_doc_len / len(docs)
        f.write(json.dumps(js, ensure_ascii=False))
