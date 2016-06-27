# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import math

vectors = None

def nearestNeighbors(vecs):
    global vectors
    vectors = vecs

def kneighbors(qry, k):
    distances = []
    for i in range(len(vectors)):
        distances.append((i, cosineSimilarity(qry, vectors[i])))
    distances.sort(key = lambda tup: tup[1], reverse=True)
    indices = []
    for i in (range(len(vectors)) if k > len(vectors) else range(k)):
        index, distance = distances[i]
        indices.append(index)
    return indices

def cosineSimilarity(v1, v2):
    return dot(v1, v2) / (np.sqrt(dot(v1, v1)) * np.sqrt(dot(v2, v2)))

def dot(v1, v2):
    return np.dot(v1, v2.T)[0]
