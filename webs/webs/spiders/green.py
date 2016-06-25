import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    T = 16
    for i in range( 1 , T+1 ):
        res.append( "http://www.greenparty.org.tw/news?page=%d" % i )
    return res

class GREENSpider(scrapy.Spider):
    name = 'green'
    allowed_domains = ['www.greenparty.org.tw']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        for href in response.css( 'div.field-content > a::attr("href")' ):
            n_page += 1
            url = response.urljoin( href.extract() )
            print( "url" , url , type( url ) )
            yield scrapy.Request( url , callback=self.parse_post )
        print( response.url , "n_page" , n_page )

    def parse_post( self , response ):
        print( "parse_post " , response.url )
        text = response.css( 'article' ).extract()[ 0 ]
        text = remove_tags( text )
        print( "text" , text )
        yield { "text" : text }
