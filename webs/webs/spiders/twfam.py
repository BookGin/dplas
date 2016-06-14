import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    T1  = 14
    T2  = 4
    for i in range( 1 , T1+1 ):
        res.append( "https://taiwanfamily.com/category/news-report/page/%d" % i )
    for i in range( 1 , T2+1 ):
        res.append( "https://taiwanfamily.com/category/latest-news/page/%d" % i )
    return res

class TWFAMSpider(scrapy.Spider):
    name = 'twfam'
    allowed_domains = ['taiwanfamily.com']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        for href in response.css( 'div > div.post-thumbnail > a::attr("href")' ):
            n_page += 1
            url = href.extract()
            print( "url" , url , type( url ) )
            yield scrapy.Request( url , callback=self.parse_post )
        print( response.url , "n_page" , n_page )

    def parse_post( self , response ):
        print( "parse_post " , response.url )
        text = ''.join( response.css( 'div.entry-inner > p' ).extract() )
        text = remove_tags( text )
        print( "text" , text )
        yield { "text" : text }



