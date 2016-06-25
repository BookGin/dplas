#encoding=utf-8
import jieba
import jieba.analyse
import os
import json
import sys


jieba.set_dictionary('dict.txt.big')

allWords = {}
wordCount = 0
allDocs = []


############      Function      #############

def parseText( text ):
    # parse document text
    # return { word : # }
    global wordCount

    wordt = {}
    words = jieba.cut(text, cut_all=False) # use cut_for_search?
    for w in words:
        if w in allWords:
            if allWords[w] in wordt:
                wordt[ allWords[w] ] += 1
            else:
                wordt[ allWords[w] ] = 1
        else:
            wordCount += 1
            allWords[ w ] = wordCount
            wordt[ wordCount ] = 1

    return wordt

def procFB( file ): # parse facebook 
    with open( file , 'r' ) as fb_data:
        jsonD = json.load( fb_data )
        for obj in jsonD[ 'posts' ]:
            mm = parseText( obj )
            allDocs.append( mm )

        print( jsonD[ 'name' ]  + ' is done. ' )
        fb_data.close()


def procWeb( file ): # parse website
    with open( file, 'r' ) as data:
        jsonD = json.load( data )
        for obj in jsonD:
            mm = parseText( obj[ 'text' ] )
            allDocs.append( mm )

        data.close()

def portRep( file ):
    with open( file, 'r' ) as data:
        jsonD = json.load( data )
        for obj in jsonD:
            str = ''
            for cont in obj[ 'content' ]:
                str += cont
            mm = parseText( str )
            allDocs.append( mm )

        data.close()


##########   Main   ##########

def check( file ):
    while not os.path.exists( file ):
        file = input( '!!! Oops, the file ' + file + ' does not exist... Please enter again (leave blank for cancellation): ' )
        if len(file) == 0:
            return ''
    return file


docUsedNum = 0

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
    output.write( str(len(allDocs))  + '\n' )

    for doc in allDocs:
        output.write( str(docUsedNum) + ' ' + str(len(doc)) + '\n' )
        docUsedNum += 1
        for tn in doc:
            output.write( str(tn) + ' ' + str(doc[ tn ]) + '\n' ) 
    
    output.close()

    print( '------------------------------------------------' )
    next = input( '>>> Continue? (Y/N) ' ).lower()
    while next != 'n' and next != 'y':
        next = input( '>>> Continue? (Y/N) ' ).lower()

    if next == 'n':
        break


# write word list

wordlist = open( 'word.list', 'w' )

for word in allWords:
    wordlist.write( word + '\n')

wordlist.close()

print( 'inverted file done.' )
