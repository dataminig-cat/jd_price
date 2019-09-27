from crawler import Runner
import schedule
import time
test_url =['https://item.jd.com/100006581142.html',
'https://item.jd.com/43769837874.html',
'https://item.jd.com/39869037975.html' ,
]

# 每天运行一次
runner = Runner()
# schedule.every(1).day.at("00:00").do(runner.run)
# schedule.every(5).seconds.do(runner.run)
schedule.every(1).days.do(runner.run)
while True:
    schedule.run_pending()
    time.sleep(5)