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

# 搜索商品
class SGoodsSpider(Spider):
    name = 'sgoods'
    def parse(self, response):
        items = []
        response.encoding = 'utf-8'
        rsp = etree.HTML(response.text)
        elems = rsp.xpath('//li[contains(@class, "gl-item")]')
        for item in elems:
            try:
                info = dict()
                info['title'] = ''.join(item.xpath('.//div[@class="p-name p-name-type-2"]//em//text()'))
                info['img'] = 'https:'+item.xpath('.//div[@class="p-img"]/a/img/@source-data-lazy-img')[0]
                info['url'] = 'https:' + item.xpath('.//div[@class="p-name p-name-type-2"]/a/@href')[0]
                info['store'] = item.xpath('.//div[@class="p-shop"]/span/a/text()')[0]
                info['store_url'] = 'https' + item.xpath('.//div[@class="p-shop"]/span/a/@href')[0]
                info['item_id'] = info.get('url').split('/')[-1][:-5]
                info['price'] = item.xpath('.//div[@class="p-price"]//i/text()')[0]
                info['comments'] = []
                # self.mongo_collection.insert_one(info)
                items.append(info)
            # 实际爬取过程中有一些广告, 其中的一些上述字段为空
            except IndexError:
                print('item信息不全, drop!')
                continue
        yield items
if __name__ == '__main__':
    pass