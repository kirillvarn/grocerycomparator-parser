import maxima, rimi, selver, prisma
from threading import Thread

from db import log_products

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

def job_init_listener(event):
    if event.exception:
        print(f"Failed. Stacktrace: {event.exception}")


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


now_dt = datetime.now()
next_4am = None

if now_dt.hour < 4 and now_dt.hour > 0:
    next_4am = datetime(now_dt.year, now_dt.month, now_dt.day, 4)
else:
    time_d = timedelta(days=1)
    next_4am = datetime(now_dt.year, now_dt.month, now_dt.day, 4) + time_d

sched = BackgroundScheduler(daemon=True)
sched.add_job(run, 'interval', start_date=next_4am, days=1)
sched.add_listener(job_init_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
sched.start()