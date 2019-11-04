from crawler.core.downloader import get_page
from crawler.core import Request
from lxml import etree

url = ''
rqs = Request(url)
rsp = get_page(rqs)
if rsp is not None:
    html = etree.HTML(rsp.text)
'https://search.jd.com/Search?keyword=%s&enc=utf-8&page=%d' % (self.v.get(), 1)

