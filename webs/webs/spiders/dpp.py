import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    for i in range( 3000 , 8979 ):
        res.append( "http://www.dpp.org.tw/news_content.php?sn=%d" % i )
    return res

class DPPSpider(scrapy.Spider):
    name = 'dpp'
    allowed_domains = ['www.dpp.org.tw']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        text = remove_tags( response.css( "#listin" ).extract()[ 0 ] )
        print( "text" , text )
        yield { "text" : text }
