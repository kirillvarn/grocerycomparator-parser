import requests as req
from db import *

# disable warnings
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# variables
URL = "http://api.hiiumaa.ecoop.ee/supermarket/products?language=et&page="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}


def get():
    products = list()

    page = 1
    while True:
        data = req.get(URL + str(page), headers=headers, timeout=60, verify=False)
        response = data.json()["data"]

        if len(response) == 0:
            break

        for product in response:
            if product["price_sale"] != None:
                discount = True
                price = product["price_sale"]
            else:
                discount = False
                price = product["price"]

            products.append(
                {
                    "id": product["id"],
                    "name": product["name"],
                    "image_url": product["image"],
                    "url": compose_url(product),
                    "tags": compose_tags,
                    "price": price,
                    "discount": discount,
                }
            )

        page += 1

    return products


##
# Helper functions
##


def compose_url(product) -> str:
    return f"https://hiiumaa.ecoop.ee/et/toode/{product['id2']}-{product['slug']}"


def compose_tags(product) -> list[str]:
    lowercase_names = map(lambda name: name.lower(), product)

    return list(lowercase_names)
