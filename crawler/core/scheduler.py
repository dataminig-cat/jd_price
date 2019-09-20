from queue import Queue #线程安全队列
class Scheduler:
    def __init__(self):
        self.queue = Queue()

    # 长度
    def __len__(self):
        return self.queue.qsize()
    def has_pending_requests(self):
        return len(self) > 0

    # 存取
    def enqueue_request(self,request):
        self.queue.put(request)
    def next_request(self):
        return self.queue.get()

    # 开闭
    def open(self, spider):
        self.spider = spider
    def close(self,reason):
        pass