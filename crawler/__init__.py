from crawler.downloader import get_page
from crawler.spiders import HtmlParser
from urllib.parse import urlsplit
def run(urls):
    # 开启调度：无
    params = {'skuIds': ''}
    for i,url in enumerate(urls):
        # 获取名称
        # 获取价格
        skuIds = urlsplit(url)[2][1:-5]
        rsp = get_page( 'https://p.3.cn/prices/mgets', params={'skuIds':skuIds})
        price = float(rsp.json()[0]['p'])   #单个商品

        # 存入数据库

        # 输出日志

if __name__ == '__main__':
    # 价格
    # url = 'https://p.3.cn/prices/mgets'
    # # 10个为一批
    # params = {'skuIds': 'J_100003883459,J_100003883459,J_35654974941,J_100004460494,J_8736570,J_7343287,J_100006976216,J_6772447,J_7296288,J_1351158,J_4354506',}
    # rsp = get_page(url, params=params)
    # print(rsp.json())
    run(['https://item.jd.com/100006581142.html'])
