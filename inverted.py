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

def procFB( dir ): # parse facebook
    for file in os.listdir( dir ):
        with open( os.path.join( dir, file ), 'r' ) as fb_data:
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

docUsedNum = 0

while True:
    outfile = input( '>>> Output inverted file: ' )
    fb_dir = input( '>>> FB directory: ' )
    web_files = input( '>>> Web file (use whitespace to split): ' )
    report_files = input( '>>> Report file (use whitespace to split): ' )

    output = open( outfile , 'w' )

    if len( fb_dir ) == 0:
        procFB( fb_dir )
    
    for web_file in web_files.split():
        procWeb( web_file )

    for report in report_files.split():
        procRep( report )


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
