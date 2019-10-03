from db_tools import Base,Column,INT,DATETIME,Session,VARCHAR,engine,FLOAT

class storeUrls(Base):
    __tablename__ = 'urls'
    id = Column(INT, primary_key=True, autoincrement=True)
    url = Column(VARCHAR(100))
    goods = Column(VARCHAR(500))
    common_price = Column(FLOAT(precision=12))
    expect_price = Column(FLOAT(precision=12))
    origin_time = Column(DATETIME)
    setting = Column(INT)

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

Base.metadata.create_all(engine)