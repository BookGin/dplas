import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    for i in range( 2009 , 2017 ):
        for j in range( 1 , 13 ):
            res.append( "http://www.kmt.org.tw/%d/%02d/?max-result=100" % ( i , j ) )
    return res

class KMTSpider(scrapy.Spider):
    name = 'kmt'
    allowed_domains = ['www.kmt.org.tw']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        for url in response.css( 'h3 a::attr("href")' ).re( 'http://www.kmt.org.tw/20.*blog.*' ):
            n_page += 1
            print( "href" , url , type( url ) )
            yield scrapy.Request( url , callback=self.parse_post )
        print( response.url , "n_page" , n_page )

    def parse_post( self , response ):
        print( "parse_post " , response.url )
        text = remove_tags( response.css( 'description' ).extract()[ 0 ] )
        print( "text" , text )
        yield { "text" : text }
