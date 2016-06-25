import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    # T   = 0
    T   = 2000
    query = input( '>>> Query: ' )
    res.append( "http://search.udn.com/search/searchNews4utf8.jsp?ch=udn.all&df=2&rc=" + str(T) + "&wc=80&pw=220&mc=&q=" + query + "&fp=1" )  
    return res

class UNIONSpider(scrapy.Spider):
    name = 'union'
    allowed_domains = ['udn.com']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        res = response.body.decode( 'utf-8' ) 
        print( res.split( '\r\n' )[:100] )
        flag = False
        for l in res.split( '\r\n' ):
          ll = l.split()
          if flag:
            print( l )
            yield scrapy.Request( l.split()[-1][1:-2] , callback=self.parse_post )
            n_page += 1
            flag = False
          elif len(ll) > 0 and ll[-1] == 'Array(8);':
            flag = True
          
        print( response.url , "n_page" , n_page )

    def parse_post( self , response ):
        print( "parse_post " , response.url )
        text = ''.join( response.css( '#story_body_content > p' ).extract() )
        text = remove_tags( text )
        # print( "text" , text )
        yield { "text" : text }





