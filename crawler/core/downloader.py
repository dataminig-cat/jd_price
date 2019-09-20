from fake_useragent import UserAgent,FakeUserAgentError
import requests
from requests.exceptions import ProxyError
import time
# 随机代理、随机头
def get_page(rqs):
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    headers = rqs.headers
    if not headers:
        base_headers = {
            'User-Agent':  ua.random,
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        headers = base_headers
    # print('Getting', url)
    try:
        r = requests.get(rqs.url, headers=headers,params=rqs.params,cookies=rqs.cookies)
        # print('Getting result', url, r.status_code)
        if r.status_code == 200:
            return r
    except Exception as e:# ConnectionError or ProxyError or ConnectionRefusedError:
        print(e)
        print('Crawling Failed', rqs.url)
        return None