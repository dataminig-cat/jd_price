from sqlalchemy import create_engine,INT,VARCHAR,Column,DATETIME,FLOAT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import load_setting,json
setting = load_setting()
# 初始化用
def new_db(name):

    # url = 'mysql+pymysql://' + 'root:123456@localhost:3306/'
    if not setting['db_status']:
        url = setting['url']
        engine = create_engine(url)  # ,echo =True)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute(f"CREATE DATABASE {name}")
        conn.close()

# 建立数据库后注释
new_db('jd_price')

url = setting['url'] + 'jd_price'
engine =  create_engine(url)#,echo =True)
Base = declarative_base(engine)
#创建会话
Session = sessionmaker(bind=engine)
# 定义映射类User，其继承上一步创建的Base


class Price(Base):
    __tablename__ = 'price'
    id = Column(INT, primary_key=True, autoincrement=True)
    gid = Column(INT)
    price = Column(FLOAT(precision=12))
    common_price = Column(FLOAT(precision=12))
    expect_price = Column(FLOAT(precision=12))
    date_time = Column(DATETIME)

class storeUrls(Base):
    __tablename__ = 'urls'
    id = Column(INT, primary_key=True, autoincrement=True)
    url = Column(VARCHAR(100))
    goods = Column(VARCHAR(500))
    origin_time = Column(DATETIME)
    setting = Column(INT)

if not setting['db_status']:
    Base.metadata.create_all(engine)
    setting['db_status'] = 1
    with open('setting.json', 'w') as f:
        json.dump(setting, f)
if __name__ == '__main__':
    # 建表
    Base.metadata.create_all(engine)