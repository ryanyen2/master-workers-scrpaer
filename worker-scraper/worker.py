import argparse
import datetime
from time import sleep
import random
import mysql.connector
import const
from utils import init_driver, log_search_page, scrolling_down
import pandas as pd


def init_db():
    db = mysql.connector.connect(
        host=const.DB_HOST,
        user=const.DB_USERNAME,
        database=const.DB_DATABASE,
        password=const.DB_PASSWORD,
        port=3000
    )
    cursor = db.cursor()
    return cursor, db


def scrap(scrap_account, from_date, proxy_server, interval=5, limit=float("inf")):
    # set up date
    max_date = datetime.datetime.today()
    from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")

    # initiate the driver
    driver = init_driver(proxy_server)
    sleep(random.uniform(1.3, 3.5))

    scraped_data = []
    tweet_ids = set()

    # keep searching until max_date
    end_date = from_date + datetime.timedelta(days=interval)
    refresh = 0

    while end_date <= max_date:
        scrolling_count = 0

        # log search page between start_date and end_date
        log_search_page(driver=driver, start_date=datetime.datetime.strftime(from_date, '%Y-%m-%d'), end_date=datetime.datetime.strftime(end_date, '%Y-%m-%d'), from_account=scrap_account)

        refresh += 1
        last_position = driver.execute_script("return window.pageYOffset;")
        scrolling = 1

        tweet_parsed = 0

        driver, scraped_data, tweet_ids, scrolling, tweet_parsed, scrolling_count, last_position = \
            scrolling_down(driver, scraped_data, tweet_ids, scrolling, tweet_parsed, limit, scrolling_count, last_position)

        if type(from_date) == str:
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d') + datetime.timedelta(days=interval)
        else:
            from_date = from_date + datetime.timedelta(days=interval)
        end_date = end_date + datetime.timedelta(days=interval)

    insert_db(scraped_data, scrap_account=scrap_account)
    driver.close()


def insert_db(scraped_data, scrap_account):
    # insert into database
    ProfileInsertQ = "INSERT INTO (...)(%s...) ON DUPLICATE KEY UPDATE ...=..."

    scraped_data = pd.DataFrame(scraped_data, columns=['ID', 'name', 'Timestamp', 'Text', 'TransText', 'Emojis', 'Comments', 'Likes', 'ImageLink', 'url'])

    for i, row in scraped_data.iterrows():
        if scrap_account:
            myCursor.execute(ProfileInsertQ, tuple(row))

    myDB.commit()


if __name__ == '__main__':
    myCursor, myDB = init_db()

    parser = argparse.ArgumentParser(description='Scrap tweets.')
    parser.add_argument('--from_account', type=str, help='example: @elonmusk', default=None)
    parser.add_argument('--start_date', type=str, help='%%Y-%%m-%%d', required=True)

    args = parser.parse_args()

    start_date = args.start_date
    from_account = args.from_account

    sleep(random.uniform(3.2, 5.7))
    scrap(from_date=start_date, scrap_account=from_account, proxy_server=None)
