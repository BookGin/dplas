import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = [ "http://blog.nuclearmb.org/archives" ]
    # T   = 0
    # T   = 5
    # for i in range( 1 , T+1 ):
        # res.append( "https://www.newpowerparty.tw/news_categories/%d/news" % i )
    return res

class NUCMBSpider(scrapy.Spider):
    name = 'nucmb'
    allowed_domains = ['blog.nuclearmb.org']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        for href in response.css( 'section.archives > article > h2 > a::attr("href")' ):
            n_page += 1
            # url = response.urljoin( href.extract() )
            url = href.extract()
            print( "url" , url , type( url ) )
            yield scrapy.Request( url , callback=self.parse_post )

        # print( response.url , "n_page" , n_page )
        # for href in response.css( 'span.next > a::attr("href")' ):
            # url = response.urljoin( href.extract() )
            # print( "next page url" , url , type( url ) )
            # yield scrapy.Request( url , callback=self.parse )

    def parse_post( self , response ):
        print( "parse_post " , response.url )
        # text = ''.join( response.css( 'div.container div.col-md-8 > p' ).extract() )
        text = response.css( 'div.entry-content' ).extract()[ 0 ]
        text = remove_tags( text )
        print( "text" , text )
        yield { "text" : text }




