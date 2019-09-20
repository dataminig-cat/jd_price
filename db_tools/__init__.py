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
    def query(self,**kwargs):
        return self.session.query(storeUrls).filter_by(**kwargs).all()
class Cprice:
    def __init__(self):
        self.session = Session()    #session的生命周期跟实例一样

    def insert(self,key='url = ..',**kwargs):
        var,val = key.split('=')    #变量名，取值
        inst = self.session.query(Price).filter(Price.href == val).first()
        delta = 0 # 附带比较功能
        if inst is None:
            kwargs[var] = val
            inst = Price(**kwargs)
            self.session.add(inst)
        else:
            delta = self.update(inst,**kwargs)
        self.session.commit()
        return delta

    def update(self,inst,**kwargs):
        delta = kwargs['price'] - inst.price
        inst.update_time = kwargs['origin_time']    #
        inst.price = kwargs['price']
        return delta