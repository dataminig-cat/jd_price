from crawler.core import Spider
from lxml import etree
import re
from urllib.parse import urljoin,urlsplit
class PriceSpider(Spider):
    name = 'price'
    def parse(self, response):
        yield response
    def build_rqs(self,url):
        kwargs = {}
        kwargs['url'] =  'https://p.3.cn/prices/mgets'  # 价格接口
        skuIds = urlsplit(url)[2][1:-5]
        kwargs['params'] ={'skuIds': skuIds}
        return kwargs

if __name__ == '__main__':
    pass