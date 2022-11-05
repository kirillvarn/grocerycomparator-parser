import maxima, rimi, selver, prisma
from threading import Thread

import psycopg2 as repo
import db

from datetime import date, datetime

def clear_db():
    conn = db.connect()
    cursor = conn.cursor()

    DATE = datetime.today().strftime("%Y-%m-%d")
    q = 'DROP TABLE IF EXISTS "%s";'
    q_2 = 'DELETE FROM public.updatedates WHERE u_name = %s'

    cursor.execute(q, (DATE, ))
    cursor.execute(q_2, (DATE, ))
    conn.commit()
    cursor.close()
    conn.close()

def run():
    METHOD = "none"
    th_list = []

    clear_db()

    th_list.append(Thread(target=selver.main, args=(METHOD,)))
    th_list.append(Thread(target=rimi.main, args=(METHOD,)))
    th_list.append(Thread(target=prisma.main, args=(METHOD,)))
    th_list.append(Thread(target=maxima.main, args=(METHOD,)))

    for i in th_list:
        i.start()

    for i in th_list:
        i.join()
