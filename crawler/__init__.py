from crawler.core import Cralwer
from db_tools import Curls
class Runner():
    def __init__(self,logger=None):
        self.logger = logger
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

if __name__ == '__main__':
    # 价格
    url = 'https://p.3.cn/prices/mgets'
    # 10个为一批
    params = {'skuIds': 'J_100003883459,J_100003883459,J_35654974941,J_100004460494,J_8736570,J_7343287,J_100006976216,J_6772447,J_7296288,J_1351158,J_4354506',}
    run()