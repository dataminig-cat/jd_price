from logger.logger import getMyLogger
from views import Itf   # interface，交互界面
from crawler import Runner
# 爬虫功能测试
itf = Itf()
logger = getMyLogger(itf.dfm)
crawler = Runner(logger)
itf.set_crawler(crawler)
itf.mainloop()