import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = [ "http://www.tepu.org.tw/?cat=16" ]
    T1  = 21
    T2  = 9
    # T   = 5
    for i in range( 1 , T1+1 ):
        res.append( "http://www.tepu.org.tw/?cat=16&paged=%d" % i )
    for i in range( 1 , T2+1 ):
        res.append( "http://www.tepu.org.tw/?cat=6&paged=%d" % i )
    return res

class TEPUSpider(scrapy.Spider):
    name = 'tepu'
    allowed_domains = ['www.tepu.org.tw']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        for href in response.css( 'div#content > div > h2.title > a::attr("href")' ):
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
        text = response.css( 'div.entry.clearfix' ).extract()[ 0 ]
        text = remove_tags( text )
        print( "text" , text )
        yield { "text" : text }




