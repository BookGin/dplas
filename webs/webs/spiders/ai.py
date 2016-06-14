import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    # T   = 0
    T   = 76
    for i in range( 0 , T+1 ):
        res.append( "https://www.amnesty.tw/news?page=%d" % i )
    return res

class AISpider(scrapy.Spider):
    name = 'ai'
    allowed_domains = ['www.amnesty.tw']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        for href in response.css( 'div.view-content span.field-content > a::attr("href")' ):
            n_page += 1
            url = response.urljoin( href.extract() )
            print( "url" , url , type( url ) )
            yield scrapy.Request( url , callback=self.parse_post )
        print( response.url , "n_page" , n_page )

    def parse_post( self , response ):
        print( "parse_post " , response.url )
        text = ''.join( response.css( 'div.node > div.content > p' ).extract() )
        text = remove_tags( text )
        print( "text" , text )
        yield { "text" : text }




