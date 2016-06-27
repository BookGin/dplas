#! /usr/bin/env python3
from sklearn.cluster import KMeans
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer , CountVectorizer
# from bm25 import TfidfVectorizer
from sklearn.externals import joblib

from src.helper.bigram import get_words

import json
import numpy as np
import scipy as sp
import jieba
import string

import os

N_CLUS  = 12
N_CLASS = 6

# bad_topic = [ 6 , 7 , 9 , 13 ]
bad_topic = []

# jieba.enable_parallel(4)

datas = []

if os.path.isfile( "./pkls/all_data.pkl" ):
    datas = joblib.load( "./pkls/all_data.pkl" )
else:
    for path , subdirs , files in os.walk( './data' ):
        for file in files:
            if file[ -5 : ] == ".json":
                datas += json.load( open( os.path.join( path , file ) , 'r' ) )
        print( path , subdirs , files )
    joblib.dump( datas , "./pkls/all_data.pkl" )

print( "all data done" )
print( datas[ :10 ] )
print( len( datas ) )

corpus = []

if os.path.isfile( './pkls/seg_poli_talk_corpus.pkl' ):
    corpus = joblib.load( './pkls/seg_poli_talk_corpus.pkl' )
else:
    for obj in datas:
        corpus.append( get_words( obj[ 'body' ] ) )

    joblib.dump( corpus , "./pkls/seg_poli_talk_corpus.pkl" )

print( corpus[ :10 ] )

def get_term_mat():
    # vectorizer = TfidfVectorizer( use_bm25idf=True , bm25_tf=True )
    # tf = CountVectorizer().fit_transform( corpus )
    vectorizer = TfidfVectorizer().fit( corpus )
    tfidf = vectorizer.transform( corpus )
    return ( tfidf , vectorizer )


vec = None
X = None

if os.path.isfile( './pkls/bm25_poli_talk_mat.pkl' ):
    X , vec = joblib.load( './pkls/bm25_poli_talk_mat.pkl' )
else:
    X , vec = get_term_mat()
    joblib.dump( ( X , vec ) , "./pkls/bm25_poli_talk_mat.pkl" )

print( "matrix done" )

clus = None

if os.path.isfile( './pkls/bm25_kmeans_model.pkl' ):
    clus = joblib.load( './pkls/bm25_kmeans_model.pkl' )
else:
    clus = KMeans( n_clusters=N_CLUS , n_init=N_CLUS+5 , n_jobs=6 )
    clus = clus.fit( X )
    joblib.dump( clus , "./pkls/bm25_kmeans_model.pkl" )

ids = clus.predict( X )

inv_topic = [ [] for i in range( N_CLUS ) ]

for i in range( len( ids ) ):
    inv_topic[ ids[ i ] ].append( i )

print( "cluster done" )

if __name__ == '__main__':

    cur = 0

    for obj in datas:
        obj[ 'body' ] = obj[ 'body' ].replace( '\n' , '' )
        obj[ 'body' ] = obj[ 'body' ].replace( '\r' , '' )
        obj[ 'body' ] = obj[ 'body' ].replace( '\\n' , '' )
        obj[ 'body' ] = obj[ 'body' ].replace( '\\r' , '' )
        obj[ 'topic' ] = int( ids[ cur ] )
        cur += 1

    json.dump( datas , open( 'corpus.json' , 'w' ) , ensure_ascii=False )

    print( "corpus.json done" )

    fos = [ open( "%dseg.txt" % i , 'w' ) for i in range( 15 ) ]

    for ( i , id ) in enumerate( ids ):
        fos[ id ].write( corpus[ i ] + '\n' )


