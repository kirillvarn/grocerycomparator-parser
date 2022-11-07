import naive, products, current_products
import schedule, time, datetime


current_products.update_current_products()
naive.run()
products.run()

# schedule.every().day.at("10:00").do(current_products.update_current_products)

# schedule.every(3).days.at("10:00").do(naive.run)
# schedule.every(3).days.at("10:00").do(products.run)

# while True:
#     n = schedule.idle_seconds()
#     print(f"Starting schedule in {datetime.timedelta(seconds=n)}")
#     time.sleep(n)
#     schedule.run_pending()