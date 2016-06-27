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

import sys

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


sys.stderr.write( "do model.py\n" )

logs = [ None for i in range( N_CLUS ) ]

topics = clus.predict( X )
D = clus.transform( X )

Xs = [ [] for i in range( N_CLUS ) ]
Ys = [ [] for i in range( N_CLUS ) ]

sys.stderr.write( "going to turn_to_sparse\n" )


if os.path.isfile( "./pkls/topic_train_data.pkl" ):
    ( Xs , Ys ) = joblib.load( "./pkls/topic_train_data.pkl" )
else:
    each_label = [ [] for i in range( N_CLASS ) ]

    for ( i , obj ) in enumerate( datas ):
        if obj[ 'label' ] != -1:
            each_label[ obj[ 'label' ] ].append( i )

    sys.stderr.write( "build important label doc\n" )
    for i in range( N_CLASS ):
        sys.stderr.write( "doing %d\n" % i )
        xs = [ ( D[ j ].min() , j ) for j in range( len( each_label[ i ] ) ) ]
        sys.stderr.write( "xs done\n" )
        xs.sort()
        each_label[ i ] = list( map( lambda p:p[ 1 ] , xs[ :min( len( xs ) , 6000 ) ] ) )
        sys.stderr.write( "len %d\n" % len( each_label[ i ] ) )
        for id in each_label[ i ]:
            x = X[ id ]
            topic = clus.predict( x )[ 0 ]
            Xs[ topic ].append( x )
            Ys[ topic ].append( i )

    sys.stderr.write( "go to turn_to_sparse\n" )

    for i in range( N_CLUS ):
        if len( set( Ys[ i ] ) ) == 1:
            Xs[ i ].append( csr_matrix( Xs[ i ][ 0 ].shape ) )
            Ys[ i ].append( -1 )
        Xs[ i ] = turn_to_sparse( Xs[ i ] )

    joblib.dump( ( Xs , Ys ) , "./pkls/topic_train_data.pkl" )

sys.stderr.write( "each topic sparse matrix done\n" )

for i in range( N_CLUS ):
    sys.stderr.write( 'labeled data topic %d : %d\n' % ( i , len( Ys[ i ] ) ) )

if os.path.isfile( "./pkls/log_reg_model.pkl" ):
    logs = joblib.load( "./pkls/log_reg_model.pkl" )
else:
    for i in range( N_CLUS ):
        sys.stderr.write( "now on topic %d's log reg\n" % i )
        log = LogisticRegression( class_weight="balanced" , n_jobs=-1 )
        if len( Ys[ i ] ) > 0 and i not in bad_topic:
            sys.stderr.write( "fit topic %d\n" % i )
            log = log.fit( Xs[ i ] , Ys[ i ] )
        logs[ i ] = log
    joblib.dump( logs , "./pkls/log_reg_model.pkl" )

sys.stderr.write( "log_reg model done\n" )

label_sz = [ 0 , 0 , 0 , 0 , 0 , 0 ]

for i in range( N_CLUS ):
    for y in Ys[ i ]:
        label_sz[ y ] += 1

for i in range( N_CLASS ):
    sys.stderr.write( "label %d size %d\n" % ( i , label_sz[ i ] ) )

def predict( raw_docs ):

    segged_docs = list( map( get_words , raw_docs ) )
    ds = vec.transform( segged_docs )

    topics = clus.predict( ds )

    res = []

    for i in range( len( topics ) ):
        topic = topics[ i ]
        d = ds[ i ]
        # sys.stderr.write( clus.transform( d ) )
        res.append( ( logs[ topic ].predict_proba( d ) , logs[ topic ].classes_ ) )

    return ( topics , res )






