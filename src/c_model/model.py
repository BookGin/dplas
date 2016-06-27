#! /usr/bin/env python3
from sklearn.cluster import KMeans
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer , CountVectorizer
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression

import json
import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
import jieba
import string

import os
from src.topic_cluster import *

def turn_to_sparse( A ):
    if len( A ) == 0:
        return csr_matrix( ( [] , [] , [0] ) , shape=( 0 , 0 ) )

    data = []
    idx  = []
    indptr = [ 0 ]
    cur = 0
    for a in A:
        data.extend( a.data.tolist() )
        idx.extend( a.indices.tolist() )
        cur += a.getnnz()
        indptr.append( cur )
    return csr_matrix( ( data , idx , indptr ) , shape=( len( A ) , A[ 0 ].shape[ 1 ] ) )


print( "do model.py" )

logs = [ None for i in range( N_CLUS ) ]

topics = clus.predict( X )
D = clus.transform( X )

Xs = [ [] for i in range( N_CLUS ) ]
Ys = [ [] for i in range( N_CLUS ) ]

print( "going to turn_to_sparse" )


if os.path.isfile( "./pkls/topic_train_data.pkl" ):
    ( Xs , Ys ) = joblib.load( "./pkls/topic_train_data.pkl" )
else:
    each_label = [ [] for i in range( N_CLASS ) ]

    for ( i , obj ) in enumerate( datas ):
        if obj[ 'label' ] != -1:
            each_label[ obj[ 'label' ] ].append( i )

    print( "build important label doc" )
    for i in range( N_CLASS ):
        print( "doing %d" % i )
        xs = [ ( D[ j ].min() , j ) for j in range( len( each_label[ i ] ) ) ]
        print( "xs done" )
        xs.sort()
        each_label[ i ] = list( map( lambda p:p[ 1 ] , xs[ :3000 ] ) )
        print( "len %d" % len( each_label[ i ] ) )
        for id in each_label[ i ]:
            x = X[ id ]
            topic = clus.predict( x )[ 0 ]
            Xs[ topic ].append( x )
            Ys[ topic ].append( i )

    print( "go to turn_to_sparse" )

    for i in range( N_CLUS ):
        if len( set( Ys[ i ] ) ) == 1:
            Xs[ i ].append( csr_matrix( Xs[ i ][ 0 ].shape ) )
            Ys[ i ].append( -1 )
        Xs[ i ] = turn_to_sparse( Xs[ i ] )

    joblib.dump( ( Xs , Ys ) , "./pkls/topic_train_data.pkl" )

print( "each topic sparse matrix done" )

for i in range( N_CLUS ):
    print( 'labeled data topic %d : %d' % ( i , len( Ys[ i ] ) ) )

if os.path.isfile( "./pkls/log_reg_model.pkl" ):
    logs = joblib.load( "./pkls/log_reg_model.pkl" )
else:
    for i in range( N_CLUS ):
        print( "now on topic %d's log reg" % i )
        log = LogisticRegression( class_weight="balanced" , n_jobs=-1 )
        if len( Ys[ i ] ) > 0 and i not in bad_topic:
            print( "fit topic %d" % i )
            log = log.fit( Xs[ i ] , Ys[ i ] )
        logs[ i ] = log
    joblib.dump( logs , "./pkls/log_reg_model.pkl" )

print( "log_reg model done" )

label_sz = [ 0 , 0 , 0 , 0 , 0 , 0 ]

for i in range( N_CLUS ):
    for y in Ys[ i ]:
        label_sz[ y ] += 1

for i in range( N_CLASS ):
    print( "label %d size %d" % ( i , label_sz[ i ] ) )

def predict( raw_docs ):

    segged_docs = list( map( get_words , raw_docs ) )
    ds = vec.transform( segged_docs )

    topics = clus.predict( ds )

    res = []

    for i in range( len( topics ) ):
        topic = topics[ i ]
        d = ds[ i ]
        # print( clus.transform( d ) )
        res.append( ( logs[ topic ].predict_proba( d ) , logs[ topic ].classes_ ) )

    return ( topics , res )






