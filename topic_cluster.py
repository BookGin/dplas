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

N_CLUS  = 15
N_CLASS = 6

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕】〞︰︱︳﹐､﹒
            ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
            々∥•‧ˇˉ─--′』」([{£¥'"‵〈《「『【〔【（［｛￡￥〝︵︷︹︻
            ︽︿﹁﹃﹙﹛﹝（｛「『-—_…''')

punct.union( string.punctuation )
punct.union( string.whitespace )

jieba.enable_parallel(4)

def get_words( text ):
    raw_words = jieba.cut_for_search( text )
    return " ".join( filter( lambda s:s not in punct , raw_words ) )

datas = []

if os.path.isfile( "all_data.pkl" ):
    datas = joblib.load( "all_data.pkl" )
else:
    for path , subdirs , files in os.walk( './data' ):
        for file in files:
            if file[ -5 : ] == ".json":
                datas += json.load( open( os.path.join( path , file ) , 'r' ) )
        print( path , subdirs , files )
    joblib.dump( datas , "all_data.pkl" )

print( "all data done" )
print( datas[ :10 ] )
print( len( datas ) )

corpus = []

if os.path.isfile( 'seg_poli_talk_corpus.pkl' ):
    corpus = joblib.load( './seg_poli_talk_corpus.pkl' )
else:
    for obj in datas:
        corpus.append( get_words( obj[ 'body' ] ) )

    joblib.dump( corpus , "seg_poli_talk_corpus.pkl" )

print( corpus[ :10 ] )

def get_term_mat():
    # vectorizer = TfidfVectorizer( use_bm25idf=True , bm25_tf=True )
    # tf = CountVectorizer().fit_transform( corpus )
    vectorizer = TfidfVectorizer().fit( corpus )
    tfidf = vectorizer.transform( corpus )
    return ( tfidf , vectorizer )


vec = None
X = None

if os.path.isfile( './bm25_poli_talk_mat.pkl' ):
    X , vec = joblib.load( './bm25_poli_talk_mat.pkl' )
else:
    X , vec = get_term_mat()
    joblib.dump( ( X , vec ) , "bm25_poli_talk_mat.pkl" )

print( "matrix done" )

clus = None

if os.path.isfile( './bm25_kmeans_model.pkl' ):
    clus = joblib.load( './bm25_kmeans_model.pkl' )
else:
    clus = KMeans( n_clusters=N_CLUS , n_init=N_CLUS+5 )
    clus = clus.fit( X )
    joblib.dump( clus , "bm25_kmeans_model.pkl" )

print( "cluster done" )

if __name__ == '__main__':
    ids = clus.predict( X )

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

    # fos = [ open( "%d.list" % i , 'w' ) for i in range( 15 ) ]

    # for ( i , id ) in enumerate( ids ):
        # fos[ id ].write( corpus[ i ] + '\n' )


