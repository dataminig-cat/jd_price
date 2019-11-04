from crawler import Runner
import schedule
import time
test_url =['https://item.jd.com/100006581142.html',
'https://item.jd.com/43769837874.html',
'https://item.jd.com/39869037975.html' ,
]

# 每天运行一次
pad = 12    # 间隔/小时
runner = Runner()
# schedule.every(1).day.at("00:00").do(runner.run)
# schedule.every(10).minutes.do(runner.run)
# schedule.every(5).seconds.do(runner.run)
schedule.every(pad).hours.do(runner.run)
# schedule.every(1).days.do(runner.run)
while True:
    runner.run()
    schedule.run_pending()
    time.sleep(3600*pad - 60)