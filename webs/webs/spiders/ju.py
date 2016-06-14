import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    T = 49
    # T = 2
    for i in range( 1 , T ):
        res.append( "http://onetaiwan.tumblr.com/page/%d" % i )
    return res

class JUSpider(scrapy.Spider):
    name = 'ju'
    allowed_domains = ['onetaiwan.tumblr.com']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        for href in response.css( 'a.post-date::attr("href")' ):
            n_page += 1
            url = href.extract()
            print( "url" , url , type( url ) )
            yield scrapy.Request( url , callback=self.parse_post )
        print( response.url , "n_page" , n_page )

    def parse_post( self , response ):
        print( "parse_post " , response.url )
        text = response.css( 'div.post-body.wysiwyg' ).extract()[ 0 ]
        text = remove_tags( text )
        print( "text" , text )
        yield { "text" : text }

