import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    T = 31
    # T = 2
    for i in range( 1 , T ):
        res.append( "http://tapcpr.org/hot-news?page=%d" % i )
    return res

class TAPCPRSpider(scrapy.Spider):
    name = 'tapcpr'
    allowed_domains = ['tapcpr.org']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        for href in response.css( 'h5.blog-listing-title > a::attr("href")' ):
            n_page += 1
            url = response.urljoin( href.extract() )
            print( "url" , url , type( url ) )
            yield scrapy.Request( url , callback=self.parse_post )
        print( response.url , "n_page" , n_page )

    def parse_post( self , response ):
        print( "parse_post " , response.url )
        text = response.css( 'div.apos-rich-text-item.apos-item' ).extract()[ 0 ]
        text = remove_tags( text )
        print( "text" , text )
        yield { "text" : text }


