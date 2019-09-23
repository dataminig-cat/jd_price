from crawler.core import Spider
from lxml import etree
# import re
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

class GoodsSpider(Spider):
    name = 'goods'
    def parse(self, response):
        item = {'href':response.url,
                'goods':''}
        html = etree.HTML(response.text)
        try:
            elems =  html.xpath('/html/body/div[6]/div/div[2]/div[1]/img')
            if elems:
                item['goods'] = elems[0].tail.strip()
            else:
                item['goods'] = html.xpath('/html/body/div[6]/div/div[2]/div[1]')[0].text.strip()


        except Exception as e:

            with open('data/goods_parse_error.txt','a',encoding='utf-8') as f:
                print(response.url,',',e,file=f)
        yield item
if __name__ == '__main__':
    pass