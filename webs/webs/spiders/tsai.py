import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    # for i in range( 1 , 2 ):
    for i in range( 1 , 15 ):
      res.append( "http://iing.tw/posts?page=%d" % i )
    return res

class TSAISpider(scrapy.Spider):
    name = 'tsai'
    allowed_domains = ['iing.tw']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        for href in response.css( 'a.post-content::attr("href")' ):
            n_page += 1
            url = response.urljoin( href.extract() )
            print( "url" , url , type( url ) )
            yield scrapy.Request( url , callback=self.parse_post )
        print( response.url , "n_page" , n_page )

    def parse_post( self , response ):
        print( "parse_post " , response.url )
        text = response.css( 'div.container.container_single-article' ).extract()[ 0 ]
        text = remove_tags( text )
        print( "text" , text )
        yield { "text" : text }

