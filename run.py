from logger.logger import getMyLogger
from views import Itf # interface，交互界面
from crawler import Runner
# 爬虫功能测试
itf = Itf()
logger = getMyLogger(itf.iFrame.dfm)
crawler = Runner(logger,itf.sFrame.add_data)
itf.set_crawler(crawler)
itf.mainloop()