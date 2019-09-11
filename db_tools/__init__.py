from db_tools.base_table import Price,Session,storeUrls
import datetime

class Curls:
    def __init__(self):
        self.session = Session()    #session的生命周期跟实例一样

    def insert_urls(self,url, status):
        insert_time = datetime.datetime.now()
        try:
            p = storeUrls(url = url, origin_time = insert_time, setting = status)
            self.session .add(p)
            self.session .commit()
        except:
            url_update = self.session .query(storeUrls).filter(url == url).first()
            url_update.origin_time = insert_time
            self.session .commit()


class Cprice:
    def __init__(self):
        pass