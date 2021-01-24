# -*- coding: utf-8 -*-

# python排程模組
from datetime import datetime, timedelta


from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()


# 匯入要排程的指令碼執行主函式
from test1 import main_job1
from test2 import main_job2
from test3 import helloworld



# 間隔3秒鐘執行一次
sched.add_job(main_job1,'interval', seconds=3)


# 間隔1分鐘執行一次
sched.add_job(main_job2,'interval', minutes=1)

#在指定的時間，只執行一次
sched.add_job(helloworld, 'date', run_date=datetime.now()+ timedelta(0,60))

# # 採用cron的方式執行
sched.add_job(helloworld, 'cron', day_of_week='4', second='*/4')


# 上面是通過add_job()來新增作業，另外還有一種方式是通過scheduled_job()修飾器來修飾函式。


@sched.scheduled_job('interval', seconds=3)
def timed_job():
    print('我愛你！')



print('before the start funciton')
#這裡的排程任務是獨立的一個執行緒

while True:
    sched.start()