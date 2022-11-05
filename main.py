import naive, products, schedule, current_products


def test():
    print("test")

schedule.every().minute.at(":30").do(test)

# schedule.every().day.at("10:00", "Europe/Tallinn").do(current_products.update_current_products

# schedule.every(3).days.at("10:00", "Europe/Tallinn").do(naive.run)
# schedule.every(3).days.at("10:00", "Europe/Tallinn").do(products.run)