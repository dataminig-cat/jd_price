from lxml import etree
import re
from urllib.parse import urljoin

def urlParse():
    pass


class HtmlParser(object):
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # 获取所有的链接
        # 格式如:<a target="_blank" title="华为（HUAWEI）..." href="//item.jd.com/12943624333.html">
        links = soup.find_all('a', href=re.compile(r"//item.jd.com/\d+\.htm"))

        # 遍历转化为完整的URL
        for link in links:
            new_url = link['href']
            new_full_url = urljoin(page_url, new_url)
            # 将结果存到一个新的列表里
            new_urls.add(new_full_url)

        return new_urls

    def _new_data(self, page_url, soup):
        res_data = {}

        # URL
        res_data['url'] = page_url

        # 匹配标题
        # <div class="sku-name">华为(HUAWEI) MateBook X 13英寸超轻薄微边框笔记本(i5-7200U 4G 256G 拓展坞 2K屏 指纹 背光 office)灰</div>
        title_node = soup.find('div', class_="sku-name")
        res_data['title'] = title_node.get_text()

        # 匹配价格
        # <div class="dd">
        # <span class="p-price"><span>￥</span><span class="price J-p-7430495">4788.00</span></span>
        """下载的网页源码无价格信息<span class="price J-p-7430495"></span></span>!!!!!"""
        price_node = soup.find('span', class_=re.compile(r"price\sJ\-p\-\d+"))
        res_data['price'] = price_node.get_text()

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser')
        new_urls = self._get_new_urls(page_url, soup)
        _new_data = self._new_data(page_url, soup)

        return new_urls, _new_data
