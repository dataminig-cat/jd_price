import logging
import time

from smtplib import SMTP    # manages a connection to an SMTP or ESMTP server.


# 自定义数据库连接日志
class MysqlHandler(logging.Handler):
    def __init__(self,itf):
        self.itf = itf
        super().__init__()
        self.nums = {}

    def emit(self, record):
        try:
            # 输出到日志界面
            date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(record.created))
            msg = self.format(record)
            id, *msg = msg.split('--')
            num = self.nums.get(id,0) + 1 #序号
            self.nums[id] = num
            # 分解
            # print(id,num,msg)
            self.itf.insert(id,tuple([num,date]+msg))
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
    handler = MysqlHandler(itf)
    handler.setLevel(logging.DEBUG)
    # 输出格式
    # fmt = logging.Formatter('%s')   #可查看大部分字段
    # fmt = logging.Formatter('%(asctime)s -- %(message)s')
    # handler.setFormatter(fmt)


    # # 给logger添加handler
    logger.addHandler(handler)
    # for i in range(10):
    #     logger.info("logger--笔记本电脑--成功")
    #     logger.info("alert--笔记本电脑--16")

    return logger


if __name__ == '__main__':
    pass
