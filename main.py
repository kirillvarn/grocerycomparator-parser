import maxima, rimi, selver, prisma
from colorama import Fore, Style
from threading import Thread
import multiprocessing as mp
from db import log_products
#from apscheduler.events import *
import time
#from apscheduler.schedulers.blocking import BlockingScheduler
#from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime, timedelta

def get_next_event(time: datetime) -> datetime:
    return time + timedelta(days=1)
now = datetime.now()
t = datetime(year=now.year, month=now.month, day=now.day, hour=4)

if now.hour > 4 or now.hour < 0:
    t = t + timedelta(days=1)

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

print(f"Starting parsing at {t}!")
until_starting = t - now
seconds_until = (until_starting.seconds) + (until_starting.days * 24 * 60 * 60)

prev_at = t

time.sleep(seconds_until)
while True:
    subprocess = mp.Process(target=run)
    subprocess.start()
    subprocess.join()
    subprocess.terminate()

    next_at = get_next_event(t)
    prev_at = next_at

    print(f"{Fore.BLUE}[INFO] Done parsing! Next parsing's at {prev_at}{Style.RESET_ALL}")
    delta_seconds = (next_at - t).days * 24 * 60 * 60
    time.sleep(delta_seconds)

