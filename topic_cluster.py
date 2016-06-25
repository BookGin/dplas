#! /usr/bin/env python3
from sklearn.cluster import KMeans
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer , CountVectorizer
# from bm25 import TfidfVectorizer
from sklearn.externals import joblib

import json
import numpy as np
import scipy as sp
import jieba
import string

import os

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕】〞︰︱︳﹐､﹒
            ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
            々∥•‧ˇˉ─--′』」([{£¥'"‵〈《「『【〔【（［｛￡￥〝︵︷︹︻
            ︽︿﹁﹃﹙﹛﹝（｛「『-—_…''')

punct.union( string.punctuation )
punct.union( string.whitespace )

def get_words( text ):
    raw_words = jieba.cut_for_search( text )
    return " ".join( filter( lambda s:s not in punct , raw_words ) )

poli = json.load( open( "./politics.json" , "r" ) )
talk = json.load( open( "./talk.json" , "r" ) )
soci = json.load( open( "./society.json" , "r" ) )

print( poli[ :10 ] )

corpus = []

if os.path.isfile( 'seg_poli_talk_corpus.pkl' ):
    corpus = joblib.load( './seg_poli_talk_corpus.pkl' )
else:
    for obj in poli:
        corpus.append( get_words( ' '.join( obj[ 'content' ] ) ) )
    for obj in talk:
        corpus.append( get_words( ' '.join( obj[ 'content' ] ) ) )
    # for obj in soci:
        # corpus.append( " ".join( jieba.cut_for_search( ' '.join( obj[ 'content' ] ) ) ) )

    joblib.dump( corpus , "seg_poli_talk_corpus.pkl" )

print( corpus[ :10 ] )

def get_term_mat():
    # vectorizer = TfidfVectorizer( use_bm25idf=True , bm25_tf=True )
    # tf = CountVectorizer().fit_transform( corpus )
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform( corpus )
    return tfidf

clus = KMeans( n_clusters=15 , n_init=20 )

X = None

if os.path.isfile( './bm25_poli_talk_mat.pkl' ):
    X = joblib.load( './bm25_poli_talk_mat.pkl' )
else:
    X = get_term_mat()
    joblib.dump( X , "bm25_poli_talk_mat.pkl" )

print( "matrix done" )

clus = None

if os.path.isfile( './bm25_kmeans_model.pkl' ):
    clus = joblib.load( './bm25_kmeans_model.pkl' )
else:
    clus = KMeans( n_clusters=15 , n_init=20 )
    clus = clus.fit( X )
    joblib.dump( clus , "bm25_kmeans_model.pkl" )

print( "cluster done" )

ids = clus.predict( X )
fos = [ open( "./bm25_clus/%d.list" % i , 'w' ) for i in range( 15 ) ]

for ( i , id ) in enumerate( ids ):
    fos[ id ].write( corpus[ i ] + '\n' )


