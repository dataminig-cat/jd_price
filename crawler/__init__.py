from crawler.downloader import get_page
from crawler.spiders import HtmlParser

if __name__ == '__main__':
    url = 'https://p.3.cn/prices/mgets'
    # 10个为一批
    params = {'skuIds': 'J_100003883459,J_100003883459,J_35654974941,J_100004460494,J_8736570,J_7343287,J_100006976216,J_6772447,J_7296288,J_1351158,J_4354506',}
    rsp = get_page(url,params=params)
    # p = HtmlParser()
    print(rsp.json())
    # a = p.parse(url,rsp.text)