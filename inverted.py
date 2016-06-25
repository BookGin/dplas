#encoding=utf-8
import jieba
import jieba.analyse
import os
import json
import sys
import string


jieba.set_dictionary('dict.txt.big')

allWords = []
docUsedNum = 0
wordCount = 0
wordL = {}

############      Function      #############

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕】〞︰︱︳﹐､﹒
            ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
            々∥•‧ˇˉ─--′』」([{£¥'"‵〈《「『【〔【（［｛￡￥〝︵︷︹︻
            ︽︿﹁﹃﹙﹛﹝（｛「『-—_…''')

punct.union( string.punctuation )
punct.union( string.whitespace )

def get_words( text ):
    raw_words = jieba.cut( text , cut_all=False )
    return list( filter( lambda s:s not in punct , raw_words ) )

def parseText( text ):
    # parse document text
    # return { word : # }
    global docUsedNum, wordCount

    words = get_words( text )

    for w in words:
        if w in wordL:
            allWords[ wordL[w] ].append( docUsedNum )
        else:
            wordL[ w ] = wordCount
            wordCount += 1
            allWords.append( [] )
            allWords[ wordL[w] ].append( docUsedNum )

    docUsedNum += 1


def procFB( file ): # parse facebook 
    with open( file , 'r' ) as fb_data:
        jsonD = json.load( fb_data )
        for obj in jsonD[ 'posts' ]:
            parseText( obj )

        print( jsonD[ 'name' ]  + ' is done. ' )
        fb_data.close()


def procWeb( file ): # parse website
    with open( file, 'r' ) as data:
        jsonD = json.load( data )
        for obj in jsonD:
            parseText( obj[ 'text' ] )

        data.close()

def portRep( file ):
    with open( file, 'r' ) as data:
        jsonD = json.load( data )
        for obj in jsonD:
            str = ''
            for cont in obj[ 'content' ]:
                str += cont
            parseText( str )

        data.close()


##########   Main   ##########

def check( file ):
    while not os.path.exists( file ):
        file = input( '!!! Oops, the file ' + file + ' does not exist... Please enter again (leave blank for cancellation): ' )
        if len(file) == 0:
            return ''
    return file



while True:
    outfile = input( '>>> Output inverted file: ' )
    print( 'Please input FB, Web or report files. Also, use whitespace to split.' )
    fb_files = input( '>>> FB file/dir: ' )
    web_files = input( '>>> Web file: ' )
    report_files = input( '>>> Report file: ' )

    output = open( outfile , 'w' )

    
    for fb_file in fb_files.split():
        fb_file = check( fb_file )
        if len( fb_file ) == 0:
            continue
        if os.path.isdir( fb_file ):
            for d in os.listdir( fb_file ):
                procFB( os.path.join( fb_file, d ) )
        else:
            procFB( fb_file )
    
    print( '   ----   FB done   ----' )

    for web_file in web_files.split():
        web_file = check( web_file )
        if len( web_file ) == 0:
            continue
        procWeb( web_file )

    print( '   ----   Web done   ----' )

    for report in report_files.split():
        report = check( report )
        if len( report ) == 0:
            continue
        procRep( report )

    print( '   ----   Report done   ----' )

    # write inverted file
    output.write( str(len(allWords))  + '\n' )

    i = 0
    for docs in allWords:
        h = {}
        for d in docs:
            if d in h:
                h[d] += 1
            else:
                h[d] = 1
        output.write( str( i ) + ' ' + str(len( h )) + ' ' + str(len( docs )) + '\n' )
        i += 1
        for d in h:
            output.write( str(d) + ' ' + str( h[d] ) + '\n' ) 
    
    output.close()

    print( '------------------------------------------------' )
    next = input( '>>> Continue? (Y/N) ' ).lower()
    while next != 'n' and next != 'y':
        next = input( '>>> Continue? (Y/N) ' ).lower()

    if next == 'n':
        break

    allWords = []


# write word list
wordlist = open( 'word.list', 'w' )

for (w,s) in sorted( wordL.items(), key=lambda v: v[1]  ):
    wordlist.write( str(s) + ' ' + w + '\n')

wordlist.close()

print( 'inverted file done.' )
