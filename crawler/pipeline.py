from crawler.core import Pipeline
from db_tools import Cprice
import datetime
from urllib.parse import urlsplit
class PricePipe(Pipeline):
    def __init__(self,**kwargs):
        super().__init__()
        self.iprice = Cprice()
        self.sperator = '--'
        self.logger = kwargs['logger']
    def itemProcess(self,rsp):
        if rsp is not None:
            name = urlsplit(rsp.url)[3].split('=')[1]
            price = float(rsp.json()[0]['p'])  # 单个商品
            insert_time = datetime.datetime.now()
            # 存入数据库
            delta = self.iprice.insert(f'href=https://item.jd.com/{name}.html', price=price, origin_time=insert_time)
            # 提醒
            if True:  # delta != 0:
                info = self.sperator.join(['alert', name, str(delta)])
                if self.logger is not None:  # 界面提醒
                    self.logger.info(info)
            # 输出日志
            if self.logger is not None:
                info = 'logger' + self.sperator + name + self.sperator + '成功'
                # print(info)
                self.logger.info(info)  # 需要对数据进行格式化
        else:
            if self.logger is not None:
                info = 'logger' + self.sperator + '' + self.sperator + '失败'
                self.logger.info(info)  # 需要对数据进行格式化