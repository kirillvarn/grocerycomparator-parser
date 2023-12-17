from parsers import *
from threading import Thread
from db import log_products, insert_current_products

from types import ModuleType

PARSERS = [selver, rimi, prisma, maxima, coop]


def run():
    threads = [Thread(target=insert, args=[parser]) for parser in PARSERS]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    log_products()


def insert(module: ModuleType) -> None:
    products = module.get()
    insert_current_products(products, module.__name__.replace("parsers.", ""))
