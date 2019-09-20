#构建请求
class Request(object):
    '''
    用于封装用户请求相关信息
    '''
    def __init__(self,url,callback=None,method='GET',headers=None,
                 cookies= None,params=None,body=None,errback=None):
        #请求方法
        self.method = str(method).upper()   #转成大写
        # 设置url
        self.url = url
        # 设置body
        if body is None:
            self._body = ''
        else:
            self._body = body
        assert callback or not errback ,"Cannot use errback without a callback"
        # 回调函数
        self.callback = callback
        # 异常回调函数
        self.errback = errback
        # 构建Header
        self.params =params or {}
        self.headers = headers or {}
        self.cookies = cookies or {}
    def callback(self):
        print('aa')
        pass