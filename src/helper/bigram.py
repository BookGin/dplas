
import string

punct = set(u'''¢、。〉》」』】〕】〞︰︱︳﹐､﹒
            ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄　﹏､～￠
            々∥•‧ˇˉ─--′』」([{£¥'"‵〈《「『【〔【（［｛￡￥〝︵︷︹︻
            ，、。．？！～＄％＠＆＃＊‧；︰…‥﹐﹒˙·﹔﹕‘’“”〝〞‵′〃◎⊕⊙○
            ●△▲▽▼☆★◇◆□︵︶︷︸︹︺︻︼︽︾︿﹀∩∪﹁﹂﹃﹄〔〕【】﹝﹞〈〉
            ﹙﹚《》（）｛｝﹛﹜『』「」＜＞≦≧﹤﹥﹣﹦≡｜∣∥–︱—︳╴¯￣﹉
            ﹊﹍﹎﹋﹌﹏︴﹨∕╲╱＼／↑↓←→↖↗↙↘
            ︽︿﹁﹃﹙﹛﹝（｛「『-—_!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~…''')

punct = punct.union( string.punctuation )
punct = punct.union( string.whitespace )
punct = punct.union( string.ascii_letters )
punct = punct.union( string.digits )

def get_words( text ):
    pure_text = '^'+''.join( w if w not in punct else ' ' for w in text )+'$'
    raw_words = []
    for i in range( 1 , len( pure_text ) ):
        raw_words.append( pure_text[ i-1:i+1 ] )
    res = " ".join( raw_words )
    res = res.replace( '\n' , '' )
    res = res.replace( '\r' , '' )
    res = res.replace( '\t' , '' )
    res = res.replace( '\\n' , '' )
    res = res.replace( '\\r' , '' )
    res = ' '.join(res.split())
    return res

