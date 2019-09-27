# 具备日志功能的爬虫
# 所有的Spiders、Pipeline等自定义对象都从配置中拿
from crawler.core.engine import Engine
from crawler.core.http import Request
from utils import load_object
class Cralwer:
    def __init__(self):
        pass
    def crawl(self,**kwargs):
        engine = Engine(self)  # 需要考虑，两个爬虫是否共用一个engine；加入self会占用很多内存
        from crawler.settings import spider,pipeline
        # 把引擎看成main函数
        # 从数据库读取链接
        if 'spider'  in kwargs:
            spider = kwargs['spider']
        spider = load_object(spider)(**kwargs)  # 需要 start_urls
        if 'pipeline' in kwargs:
            pipeline = kwargs['pipeline']
        pipeline = load_object(pipeline)(**kwargs)  # 需要logger
        engine.open_spider(spider,pipeline,iter(spider.start_requests()))


# Spider
class Spider:
    """Base class for scrapy spiders. All spiders must inherit from this
    class.
    """

    name = None
    custom_settings = None


    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def build_rqs(self,url):
        kwargs = {}
        kwargs['url'] = url
        return kwargs

    def start_requests(self):
        for url in self.start_urls:
            kwargs = self.build_rqs(url)
            yield Request(**kwargs)

    def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))


    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)

    def __str__(self):
        return "<%s %r at 0x%0x>" % (type(self).__name__, self.name, id(self))

    __repr__ = __str__

class Pipeline:
    '''管道基类'''
    def __init__(self):
        self.max =5 #同时处理数
        self.schduler =None
        self.active = set()

    def itemProcess(self,rsp):
        self.active.add(rsp)
        self._itemProcess(rsp)
        self.active.remove(rsp)

    def _itemProcess(self,rsp):
        raise NotImplemented('子类中继承')

    def is_idele(self):
        if len(self.active) < self.max:
            return True
        return False

    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline