from bs4 import BeautifulSoup
import requests as req
import re
import asyncio
import aiohttp

# global variables such as parsing URL, requests
BASE_URL = "https://www.rimi.ee"
request = req.get(BASE_URL + "/epood/en")
parser = BeautifulSoup(request.content, "html.parser")
products = list()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}


# get all the URLs for every product category
def GetCategoryURLS():
    url_array = parser.find_all("ul", id=re.compile("(desktop_category_menu_)."))
    return [x.find("a", class_="base-category-link")["href"] for x in url_array]


# service method just to keep everything clear
# gets product info (name, price) and returns dictionary
def GetProductInfo(html_code):
    # defining local parser
    product_parser = BeautifulSoup(str(html_code), "html.parser")

    name = product_parser.find("p", class_="card__name").text
    index = [
        item["data-product-code"]
        for item in product_parser.find_all("div", attrs={"data-product-code": True})
    ]
    discount = True if product_parser.find("div", class_="-has-discount") else False
    try:
        pattern = re.compile("[0-9]+")
        price = pattern.findall(
            f"{product_parser.find('div', class_='price-tag').text}"
        )
        price = f"{price[0]}.{price[1]}"
    except:
        price = 0
    return {
        "id": str(index[0]),
        "name": f"{index[0]}, {name}",
        "price": price,
        "discount": discount,
    }


async def getPageData(session, url):
    page = 1
    while True:
        async with session.get(
            url=f"{BASE_URL}/{url}?page={page}", headers=headers
        ) as response:
            response_data = await response.text()
            parser = BeautifulSoup(response_data, "html.parser")
            items = parser.find_all("li", class_="product-grid__item")

            if len(items) == 0:
                break

            for item in items:
                products.append(GetProductInfo(item))
            page += 1


async def gatherData():
    semaphore = asyncio.Semaphore(200)
    async with semaphore:
        connector = aiohttp.TCPConnector(force_close=True)
        async with aiohttp.ClientSession(
            connector=connector, trust_env=True
        ) as session:
            tasks = list()

            for url in GetCategoryURLS():
                task = asyncio.create_task(getPageData(session, url))
                tasks.append(task)

            await asyncio.gather(*tasks)


def main(method):
    asyncio.run(gatherData())
    return products
