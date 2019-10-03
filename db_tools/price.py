from db_tools import Base,Column,INT,FLOAT,DATETIME,Session,engine
class Price(Base):
    __tablename__ = 'price'
    id = Column(INT, primary_key=True, autoincrement=True)
    gid = Column(INT)
    price = Column(FLOAT(precision=12))
    date_time = Column(DATETIME)

class Cprice:
    def __init__(self):
        self.session = Session()    #session的生命周期跟实例一样

    def insert(self,**kwargs):
        inst = Price(**kwargs)
        self.session.add(inst)
        self.session.commit()

    def query(self,**kwargs):
        return self.session.query(Price).filter_by(**kwargs).all()

Base.metadata.create_all(engine)