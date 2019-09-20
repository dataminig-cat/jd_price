from crawler.core.scheduler import Scheduler
from crawler.core.downloader import get_page
from crawler.core.http import Request
# from lxml import etree
from types import GeneratorType

class Engine:
    def __init__(self,crawler,wait = 1):
        self.scheduler = Scheduler()    # 暂时只有一个队列
        # self.crawler = crawler  #
        self.downloader = get_page
        # self.wait =wait #如果没有任务了，就等待

    # 解析后回调
    def get_response_callback(self,rsp):
        if rsp is None:return
        print('队列长度',len(self.scheduler))
        # html = etree.HTML(rsp.text)
        info = self.spider.parse(rsp)   #这里需要判断是否是需要重新爬取
        if isinstance(info,GeneratorType):  # 为何
            for i in info:
                if isinstance(i,Request):
                    self.scheduler.enqueue_request(i)
                else:
                    self.pipeline.itemProcess(i)

    # 循环爬取
    def _next_request(self):
        '''循环下载request'''
        # 没有任务就返回
        if self.scheduler.has_pending_requests() and self.is_idle():
            pass
        if self.scheduler.has_pending_requests() :
            req = self.scheduler.next_request()
            if not req:
                return
            rsq = self.download(req)
            self.get_response_callback(rsq)
            self._next_request()

    # open启动函数
    def open_spider(self,spider,pipeline,start_requests):
        self.spider = spider    #后面需要用到解析
        self.pipeline = pipeline
        while True:
            try:
                req = next(start_requests)
            except StopIteration:
                break
            self.scheduler.enqueue_request(req)
        self._next_request()

    # 是否空闲
    def is_idle(self):
        return True

    # 下载
    def download(self,req):
        return self.downloader(req)