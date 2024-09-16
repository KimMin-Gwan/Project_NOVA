from data.admin import *

import schedule
import time

if __name__ == '__main__':
    client = Admin()
    data = None
    schedule.every().day.at("00:00").do(client._request(data,endpoint='/reset_daily'))
    schedule.every(14).days.at("00:00").do(client._request(data,endpoint='/reset_league_point'))
        
    while True:
        schedule.run_pending()
        time.sleep(1)