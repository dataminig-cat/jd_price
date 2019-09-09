from sqlalchemy import create_engine
url = 'mysql+pymysql://'+'root:123456@localhost:3306/'#+'jd_prcie'
engine =  create_engine(url)#,echo =True)

def new_db(name):
    conn = engine.connect()
    conn.execute("commit")
    conn.execute(f"CREATE DATABASE {name}")
    conn.close()

new_db('jd_prcie')