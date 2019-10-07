from sqlalchemy import create_engine,INT,VARCHAR,Column,DATETIME,FLOAT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import load_setting,json
setting = load_setting()

def new_db(name):
    if not setting['db_status']:
        url = setting['url']
        engine = create_engine(url)  # ,echo =True)
        conn = engine.connect()
        conn.execute("commit")
        try:
            conn.execute(f"CREATE DATABASE {name}")
        except Exception as e:
            print(e)
        conn.close()
    setting['db_status'] = 1
    with open('setting.json', 'w') as f:
        json.dump(setting, f)
# 建立数据库后注释
new_db('jd_price')

# 初始化用
url = setting['url'] + 'jd_price'
engine =  create_engine(url)#,echo =True)
Base = declarative_base(engine)
#创建会话
Session = sessionmaker(bind=engine)
# 定义映射类User，其继承上一步创建的Base
