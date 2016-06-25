import scrapy
from scrapy.utils.markup import remove_tags

def get_urls():
    res = []
    for i in range( 752 , 1586 ):
        res.append( "http://www.pfp.org.tw/TW/News/ugC_News_Detail.asp?hidNewsCatID=4&hidNewsID=%d" % i )
    return res

class PFPSpider(scrapy.Spider):
    name = 'pfp'
    allowed_domains = ['www.pfp.org.tw']
    start_urls = get_urls()

    def parse(self, response):
        n_page = 0
        text = remove_tags( response.css( "article.PageArticle" ).extract()[ 0 ] )
        print( "text" , text )
        yield { "text" : text }

