from fake_useragent import UserAgent,FakeUserAgentError
import requests
# 随机代理、随机头
def get_page(url,headers={}, params={}):
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    base_headers = {
        'User-Agent':  ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    headers = dict(base_headers)
    print('Getting', url)
    try:
        r = requests.get(url, headers=headers,params=params)
        print('Getting result', url, r.status_code)
        if r.status_code == 200:
            return r
    except ConnectionError:
        print('Crawling Failed', url)
        return None


