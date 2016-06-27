# -*- coding: utf-8 -*-
import math
import json
import sys

import bigram

issue_model = None

def load(db_path_prefix):
    global issue_model
    issue_model = IssueModel(db_path_prefix)

def measure(raw_text, topic_index):
    return issue_model.measure(raw_text, topic_index)

class IssueModel:
    OKAPI_K = 1.6
    OKAPI_B = 0.75

    vocabs = []
    doc_freqs = []
    TOTAL_DOCS = []
    AVG_DOC_LENS = []
    total_load_file = 0

    def __init__(self, path_prefix):
        while self.total_load_file >= 0:
            path = "%s/%d" % (path_prefix, self.total_load_file)
            try:
                self.vocabs.append(json.load(open( "%s.vocab" % path, 'r')))
                self.doc_freqs.append(json.load(open("%s.freq" % path, 'r')))
                misc = json.load(open("%s.misc" % path, 'r'))
                self.TOTAL_DOCS.append(misc["total_doc"])
                self.AVG_DOC_LENS.append(misc["avg_len"])
                self.total_load_file += 1
            except FileNotFoundError:
                sys.stderr.write("%d.{vocab, freq, misc} not found\n" % self.total_load_file)
                sys.stderr.write("Loaded %d inverted files successfully\n" % self.total_load_file)
                return

    def measure(self, raw_text, topic_index):
        doc = self.cut(raw_text)
        return self.getVector(doc, topic_index)

    def getTF(self, term, doc, topic_index):
        raw_tf = doc.count(term)
        return (raw_tf * (self.OKAPI_K + 1)) / (raw_tf + self.OKAPI_K * (1 - self.OKAPI_B + self.OKAPI_B * len(doc) / self.AVG_DOC_LENS[topic_index]))

    def getIDF(self, term, topic_index):
        return math.log((self.TOTAL_DOCS[topic_index] - self.doc_freqs[topic_index][term] + 0.5) / (self.doc_freqs[topic_index][term] + 0.5))

    def getTFIDF(self, term, doc, topic_index):
        return self.getTF(term, doc, topic_index) * self.getIDF(term, topic_index)

    def getVector(self, doc, topic_index):
        vec = []
        for term in self.vocabs[topic_index].keys():
            vec.append(self.getTFIDF(term, doc, topic_index))
        return vec

    def cut(self, text):
        return bigram.get_words(text).split(" ")
