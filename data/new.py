import requests
from lxml import etree

def get(page, keyword):
    """
    从搜索页获取相应信息并存入数据库
    :param page: 搜索页的页码
    :return: 商品的id
    """
    print(1111111)
    print(page, keyword)
    url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&page=%d' % (keyword, page)
    index_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'Accept-Charset': 'utf-8',
        'accept-language': 'zh,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.169 Safari/537.36'
    }
    rsp = requests.get(url=url, headers=index_headers).content.decode()
    # rsp = requests.get(url=url).content.decode()
    rsp = etree.HTML(rsp)
    items = rsp.xpath('//li[contains(@class, "gl-item")]')
    for item in items:
        try:
            info = dict()
            info['title'] = ''.join(item.xpath('.//div[@class="p-name p-name-type-2"]//em//text()'))
            info['url'] = 'https:' + item.xpath('.//div[@class="p-name p-name-type-2"]/a/@href')[0]
            info['store'] = item.xpath('.//div[@class="p-shop"]/span/a/text()')[0]
            info['store_url'] = 'https' + item.xpath('.//div[@class="p-shop"]/span/a/@href')[0]
            info['item_id'] = info.get('url').split('/')[-1][:-5]
            info['price'] = item.xpath('.//div[@class="p-price"]//i/text()')[0]
            info['comments'] = []
            print(info)
            # self.mongo_collection.insert_one(info)
            # yield info['item_id']
            print(info)
        # 实际爬取过程中有一些广告, 其中的一些上述字段为空
        except IndexError:
            print('item信息不全, drop!')
            continue

if __name__ == '__main__':
    get(1, '耳机')