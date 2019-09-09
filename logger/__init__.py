import logging
import time

# 自定义数据库连接日志
class MysqlHandler(logging.Handler):

    def emit(self, record):
        try:
            print((record))
            date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(record.created))
            print(date)
            msg = self.format(record)
            print((msg))
            # stream = self.stream
            # stream.write(msg)
            # stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


# class MyLogger:
#     def __init__(self,itf):
#         self.itf = itf
def getMyLogger(itf):
    # 创建logger
    logger = logging.getLogger('basic')
    logger.setLevel(logging.DEBUG)
    # 创建handler
    handler = MysqlHandler()
    handler.setLevel(logging.DEBUG)
    # 输出格式
    # fmt = logging.Formatter('%s')   #可查看大部分字段
    fmt = logging.Formatter('%(asctime)s -- %(message)s')
    handler.setFormatter(fmt)
    # 给logger添加handler
    logger.addHandler(handler)
    logger.info("10 - 10 - 0 ")
    return logger


