import maxima, rimi, selver, prisma
from colorama import Fore, Style
from threading import Thread

from db import log_products
from apscheduler.events import *

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime, timedelta

now_dt = datetime.now()
next_4am = None

if now_dt.hour < 4 and now_dt.hour > 0:
    next_4am = datetime(now_dt.year, now_dt.month, now_dt.day, 4)
else:
    time_d = timedelta(days=1)
    next_4am = datetime(now_dt.year, now_dt.month, now_dt.day, 4) + time_d

def run():
    th_list = []

    th_list.append(Thread(target=selver.current_products))
    th_list.append(Thread(target=rimi.current_products))
    th_list.append(Thread(target=prisma.current_products))
    th_list.append(Thread(target=maxima.current_products))

    for i in th_list:
        i.start()

    for i in th_list:
        i.join()

    log_products()
    print(f"{Fore.BLUE}[INFO] Done parsing! Next parsing's at {next_4am + timedelta(days=1)}{Style.RESET_ALL}")




sched = BlockingScheduler(
    executors={
        'threadpool': ThreadPoolExecutor(max_workers=9),
        'processpool': ProcessPoolExecutor(max_workers=3)
    }
)

sched.add_job(run, 'interval', start_date=next_4am, days=1)
print(f"Next parser: {next_4am}")
sched.start()