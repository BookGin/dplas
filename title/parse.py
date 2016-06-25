import jieba

jieba.set_dictionary('../dict.txt.big')

words = {}

file = open( './titles', 'rb' )

line = file.readline().decode( 'utf-8' )
while line:
    l = jieba.cut( line, cut_all=False ) 
    for w in l:
        if w in words:
            words[ w ] += 1
        else:
            words[ w ] = 1

    line = file.readline().decode( 'utf-8' )

file.close()

out = open( 'sort.out', 'w' )
for (w,s) in sorted( words.items(), key=lambda v: v[1], reverse=True  )[ :5000  ]:
    out.write( w + ' ' + str(s) + '\n')

out.close()
