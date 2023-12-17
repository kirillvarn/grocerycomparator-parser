from datetime import datetime
from psycopg2 import extras
import psycopg2
import time

from helpers import *

import os

DATE = datetime.today().strftime("%Y-%m-%d")
DEV = os.environ.get("FLASK_ENV") == "development"
RETRY_LIMIT = 50


def connect(retries=0, db="products"):
    if not DEV:
        user = os.getenv("PGUSER")
        password = os.getenv("PGPASSWORD")
        host = os.getenv("PGHOST")
        port = os.getenv("PGPORT")
    else:
        user = "postgres"
        password = "postgres"
        host = "localhost"
        port = "5432"
        db = "product_dev"
    try:
        CONNECTION = psycopg2.connect(
            dbname=db,
            user=user,
            password=password,
            host=host,
            port=port,
        )

        retries = 0
        return CONNECTION
    except psycopg2.OperationalError as error:
        if retries >= RETRY_LIMIT:
            raise error
        else:
            retries += 1
            time.sleep(5)
            return connect(retries=retries, db=db)
    except (Exception, psycopg2.Error) as error:
        raise error


def insert_current_products(products: list, shop: str) -> None:
    inserted_at = datetime.today().strftime("%Y-%m-%d")
    conn = connect(db="naive_products")
    cursor = conn.cursor()

    get_price = lambda price: round(cast_to_numeric(price), 2) or 0

    data = [
        (
            # Update
            get_price(entry["price"]),
            entry["discount"],
            inserted_at,
            entry["id"] + shop[0],
            get_price(entry["price"]),
            # Insert
            entry["id"] + shop[0],
            entry["name"],
            get_price(entry["price"]),
            shop,
            entry["discount"],
            inserted_at,
            entry["tags"],
            entry["url"],
            entry["image_url"]
        )
        for entry in products
    ]

    insert_q = "update current_products set price=%s, discount=%s, inserted_at=%s where id = %s and price != %s; insert into (product_id, name, price, store_name, discount, inserted_at, tags, url, image_url) current_products values (%s, %s, %s, %s, %s, %s, %s, %s, %s) on conflict (id) do nothing;"

    # insert into products

    extras.execute_batch(cursor, insert_q, data)

    conn.commit()
    cursor.close()

    conn.close()


def log_products():
    conn = connect(db="products")
    cursor = conn.cursor()

    copy_q = (
        "insert into products select * from current_products where inserted_at = %s"
    )

    cursor.execute(copy_q, (DATE,))
    conn.commit()
    cursor.close()
    conn.close()
