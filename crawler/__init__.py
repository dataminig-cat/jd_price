from crawler.core import Cralwer
from db_tools.url import Curls
class Runner():
    def __init__(self,logger=None,itf=None):
        self.logger = logger
        self.itf = itf
        self.cralwer = Cralwer()
    def get_urls(self):
        iurls = Curls()
        urls = []
        for inst in iurls.query(setting=1):
            urls.append(inst.url)
        return urls
    def run(self):
        urls = self.get_urls()
        self.cralwer.crawl(start_urls=urls, logger=self.logger)

    def set_goods_name(self,urls):
        self.cralwer.crawl(start_urls=urls,spider= 'crawler.spiders.' + 'GoodsSpider',
                           pipeline= 'crawler.pipeline.'+ 'GoodsPipe')

    def search_goods(self,urls):
        self.cralwer.crawl(start_urls=urls,spider= 'crawler.spiders.' + 'SGoodsSpider',
                           pipeline= 'crawler.pipeline.'+ 'SGoodsPipe',itf=self.itf)

if __name__ == '__main__':
    # 价格
    url = 'https://p.3.cn/prices/mgets'
    # 10个为一批
    params = {'skuIds': 'J_100003883459,J_100003883459,J_35654974941,J_100004460494,J_8736570,J_7343287,J_100006976216,J_6772447,J_7296288,J_1351158,J_4354506',}
    runner = Runner()
    test_url = ['https://item.jd.com/100006581142.html',
                'https://item.jd.com/43769837874.html',
                'https://item.jd.com/39869037975.html',
                'https://item.jd.com/39869037975.html',
                ]
    runner.set_goods_name(test_url)
