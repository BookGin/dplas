#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import bigram


# usage: ./parseJson.py "corpus.json path" "output directory"

def concatString(path):
    corpus = ""
    with open(path, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            corpus += line
    return corpus


corpus = concatString(sys.argv[1])
data = json.loads(corpus)
output_path = sys.argv[2]
topics = {}
for doc in data:
    print("topic" + str(doc["topic"]) + "docs is" + doc["body"])
    print("<end>")
    string = bigram.get_words(doc["body"])
    topic_num = doc["topic"]
    if topic_num not in topics:
        topics[topic_num] = []
    print(type(topics[topic_num]))
    topics[topic_num].append(string + "\n")
    print(topics[topic_num], end="\n\n\n\n")

print("Finish traversing corpus.json")
print(topics[10])
print("==============================")

for topic_index in topics.keys():
    path = "%s/%d.txt" % (output_path, topic_index)
    with open(path, 'w', encoding='UTF-8') as f:
        f.writelines(topics[topic_index])

print("Generated %d files." % len(topics))
