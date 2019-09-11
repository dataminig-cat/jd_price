from db_tools.base_table import Price,Session,storeUrls
import datetime

class Curls:
    def __init__(self):
        self.session = Session()    #session的生命周期跟实例一样

    def insert_urls(self,url, status):
        insert_time = datetime.datetime.now()
        inst = self.session .query(storeUrls).filter(storeUrls.url == url).first()
        if inst is None:
            p = storeUrls(url = url, origin_time = insert_time, setting = status)
            self.session .add(p)
            self.session .commit()
        else:
            inst.origin_time = insert_time
            self.session .commit()


class Cprice:
    def __init__(self):
        self.session = Session()    #session的生命周期跟实例一样

    def insert(self,key='url = ..',**kwargs):
        var,val = key.split('=')    #变量名，取值
        inst = self.session.query(Price).filter(Price.href == val).first()
        if inst is None:
            inst = Price(**kwargs)
            self.session.add(inst)
        else:
            self.update(inst,**kwargs)
        self.session.commit()

    def update(self,inst,**kwargs):
        inst.update_time = kwargs['update_time']    #
        inst.price = kwargs['price']
