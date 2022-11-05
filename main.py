# import naive, products, schedule, current_products
import schedule, time

schedule.every().day.at("10:00", "Europe/Tallinn").do(current_products.update_current_products

schedule.every(3).days.at("10:00", "Europe/Tallinn").do(naive.run)
schedule.every(3).days.at("10:00", "Europe/Tallinn").do(products.run)

while True:
    n = schedule.idle_seconds()
    time.sleep(n)
    schedule.run_pending()