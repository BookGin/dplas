import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    # T   = 0
    T   = 700
    for i in range( 1 , T+1 ):
        res.append( "http://search.udn.com/search/searchNews4utf8.jsp?ch=udn.key&df=2&rc=500&wc=1&pw=2&mc=&q=的&fp=%d" % i )
    return res

class UDNSpider(scrapy.Spider):
    name = 'udn'
    allowed_domains = ['search.udn.com','udn.com']
    start_urls = get_urls()

    def parse(self, response):
        # print( response.body.decode( 'utf-8' ) )
        strs = list( filter( lambda s:s.startswith( 'arr' ) , response.body.decode( 'utf-8' ).split( '\r\n' ) ) )
        # print( list( strs ) )
        n_page = 0
        for i in range( 0 , len( strs ) , 9 ):
            if '要聞' in strs[ i+4 ]:
                url = strs[ i+1 ].split()[ -1 ][ 1 : -2 ]
                yield scrapy.Request( url , callback=self.parse_post )
        print( response.url , "n_page" , n_page )

    def parse_post( self , response ):
        print( "parse_post " , response.url )
        text = ' '.join( filter( lambda s:'function' not in s , response.css( 'div#story_body p' ).extract() ) )
        text = remove_tags( text )
        print( "text" , text )
        yield { "text" : text }





