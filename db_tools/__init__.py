from db_tools.base_table import Price,Session,storeUrls
import datetime

class Curls:
    def __init__(self):
        self.session = Session()    #session的生命周期跟实例一样

    def update(self,key='url = ..',**kwargs):
        var,val = key.split('=')    #变量名，取值
        inst = self.session.query(storeUrls).filter(storeUrls.url == val).first()
        delta = 0 # 附带比较功能
        if inst is None:
            kwargs[var] = val
            inst = storeUrls(**kwargs)
            self.session.add(inst)
        else:
            # inst.__dict__.update(kwargs)    # 无效
            for k,v in kwargs.items():
                exec(f'inst.{k}="{v}"')
            delta = self.update_(inst)
        self.session.commit()
        return delta
    def update_(self,inst):
        return 0
    def query(self,**kwargs):
        return self.session.query(storeUrls).filter_by(**kwargs).all()
class Cprice:
    def __init__(self):
        self.session = Session()    #session的生命周期跟实例一样

    def insert(self,**kwargs):
        inst = Price(**kwargs)
        self.session.add(inst)
        self.session.commit()

    def query(self,**kwargs):
        return self.session.query(Price).filter_by(**kwargs).all()