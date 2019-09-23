from crawler.core import Pipeline
from db_tools import Curls,Cprice,datetime,Price
from urllib.parse import urlsplit
class PricePipe(Pipeline):
    def __init__(self,**kwargs):
        super().__init__()
        self.iprice = Cprice()
        self.iurls = Curls()
        self.sperator = '--'
        self.logger = kwargs['logger']
    def itemProcess(self,rsp):
        if rsp is not None:
            skuid = urlsplit(rsp.url)[3].split('=')[1]
            price = float(rsp.json()[0]['p'])  # 单个商品
            href = f'https://item.jd.com/{skuid}.html'
            # 商品id
            inst = self.iurls.query(url=href)[0]
            insert_time = datetime.datetime.now()
            # 存入数据库
            self.iprice.insert(gid=inst.id, price=price, date_time=insert_time)
            # 价格变化
            delta = 0
            price_inst = self.iprice.session.query(Price).\
                filter(Price.gid==inst.id).order_by(Price.id.desc()).first()
            if price_inst is not None:
                delta =price - price_inst.price
            # 提醒
            if True:  # delta != 0:
                info = self.sperator.join(['alert', inst.goods, str(delta)])
                if self.logger is not None:  # 界面提醒
                    self.logger.info(info)
            # 输出日志
            if self.logger is not None:
                info = 'logger' + self.sperator + inst.goods + self.sperator + '成功'
                # print(info)
                self.logger.info(info)  # 需要对数据进行格式化
        else:
            if self.logger is not None:
                info = 'logger' + self.sperator + '' + self.sperator + '失败'
                self.logger.info(info)  # 需要对数据进行格式化

class GoodsPipe(Pipeline):
    def __init__(self,**kwargs):
        super().__init__()
        self.iurls = Curls()
    def itemProcess(self,rsp):
        if rsp is not None:
            insert_time = datetime.datetime.now()
            # 存入数据库
            self.iurls.update(f'url={rsp["href"] }',goods=rsp['goods'],origin_time=insert_time)