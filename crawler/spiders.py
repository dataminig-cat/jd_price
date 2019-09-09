from lxml import etree
import re
from urllib.parse import urljoin

def urlParse():
    pass


class HtmlParser(object):
    def _get_new_urls(self, page_url, html):
        new_urls = set()
        # 获取所有的链接
        # 格式如:<a target="_blank" title="华为（HUAWEI）..." href="//item.jd.com/12943624333.html">
        links = html.xpath('a', href=re.compile(r"//item.jd.com/\d+\.htm"))

        # 遍历转化为完整的URL
        for link in links:
            new_url = link['href']
            new_full_url = urljoin(page_url, new_url)
            # 将结果存到一个新的列表里
            new_urls.add(new_full_url)

        return new_urls

    def _new_data(self, page_url, eroot):
        res_data = {}

        # URL
        res_data['url'] = page_url

        # 匹配标题
        # <div class="sku-name">华为(HUAWEI) MateBook X 13英寸超轻薄微边框笔记本(i5-7200U 4G 256G 拓展坞 2K屏 指纹 背光 office)灰</div>
        title_node = eroot.xpath('/html/body/div[6]/div/div[2]/div[1]')
        if title_node:
            res_data['title'] = title_node[0].text.strip()
        price_node = eroot.xpath('/html/body/div[6]/div/div[2]/div[4]/div/div[1]/div[2]/span[1]/span[2]')
        if price_node:
            return price_node
            res_data['price'] = price_node[0].text.strip()
        print(res_data)

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        eroot = etree.HTML(html_cont)
        # new_urls = self._get_new_urls(page_url, eroot)
        _new_data = self._new_data(page_url, eroot)

        return  _new_data

class PriceParse:
    def __init__(self):
        pass

    def parse(self):
        pass
