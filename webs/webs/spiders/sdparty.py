import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    for i in range( 2 , 269 ):
        res.append( "https://www.sdparty.tw/articles/%d" % i )
    return res

class SDPARTYSpider(scrapy.Spider):
    name = 'sdparty'
    allowed_domains = ['www.sdparty.tw']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        text = remove_tags( response.css( "div.col-md-12.editor-block" ).extract()[ 0 ] )
        print( "text" , text )
        yield { "text" : text }


