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
from topic_cluster import *

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

Xs = [ [] for i in range( N_CLUS ) ]
Ys = [ [] for i in range( N_CLUS ) ]

print( "going to turn_to_sparse" )

if os.path.isfile( "topic_train_data.pkl" ):
    Xs = joblib.load( "topic_train_data.pkl" )
else:
    each_label = [ [] for i in range( N_CLASS ) ]

    for ( i , obj ) in enumerate( datas ):
        if obj[ 'label' ] != -1:
            each_label[ obj[ 'label' ] ].append( X[ i ] )

    def important( x ):
        dis = clus.transform( x )
        return dis.min()

    print( "build important label doc" )
    
    for i in range( N_CLASS ):
        print( "doing %d" % i )
        xs = [ ( important( each_label[ i ][ j ] ) , j ) for j in range( len( each_label[ i ] ) ) ]
        print( "xs done" )
        xs.sort()
        each_label[ i ] = map( lambda p:p[ 1 ] , xs[ :3000 ] )
        print( "len %d" % len( each_label[ i ] ) )
        for x in each_label[ i ]:
            topic = clus.predict( x )[ 0 ]
            Xs[ topic ].append( x )
            Ys[ topic ].append( i )

    print( "go to turn_to_sparse" )

    for i in range( N_CLUS ):
        Xs[ i ] = turn_to_sparse( Xs[ i ] )

    joblib.dump( Xs , "topic_train_data.pkl" )

print( "each topic sparse matrix done" )

for i in range( N_CLUS ):
    print( 'labeled data topic %d : %d' % ( i , len( Xs[ i ] ) ) )

if os.path.isfile( "log_reg_model.pkl" ):
    logs = joblib.load( "log_reg_model.pkl" )
else:
    for i in range( N_CLUS ):
        print( "now on topic %d's log reg" % i )
        log = LogisticRegression( n_jobs=-1 )
        if len( Ys[ i ] ) > 0:
            log = log.fit( Xs[ i ] , Ys[ i ] )
        logs[ i ] = log
    joblib.dump( logs , "log_reg_model.pkl" )

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
        res.append( logs[ topic ].predict_proba( d ) )

    return res





