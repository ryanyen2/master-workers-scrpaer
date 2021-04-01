from time import sleep
import random
import mysql.connector
import const
from datetime import datetime
from dateutil.relativedelta import relativedelta
import docker

from utils import init_driver, fetch_search_page, check_new_update


def init_db():
    # set to local db (host will base on your environment)
    myDB = mysql.connector.connect(
        host=const.DB_HOST,
        user=const.DB_USERNAME,
        database=const.DB_DATABASE,
        password=const.DB_PASSWORD,
        port=3306
    )
    myCursor = myDB.cursor()

    # target account table to scrap (ex: @elonmusk, @obama...)
    # myCursor.execute("CREATE TABLE IF NOT EXISTS `fetching_list` (...) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")

    # table to store the data
    # myCursor.execute("CREATE TABLE IF NOT EXISTS `store_data` (..schema...) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")

    myCursor.execute("SELECT * FROM fetching_list")
    account_to_fetch = myCursor.fetchall()

    return myCursor, myDB, account_to_fetch


# from_accounts = (id, account_name)
def fetch_last_timestamp(from_accounts):
    # see the last timestamp from the latest scraped data
    myCursor.execute("SELECT from_account, MAX(Timestamp) FROM store_data GROUP BY from_account")
    last_time_data = myCursor.fetchall()

    # check if the to_scrap_account hasn't appear in the store_data => set last_timestamp = None
    for fc in from_accounts:
        if fc[1] not in [temp[0] for temp in last_time_data]:
            last_time_data.append((fc[1], None))

    return last_time_data


def render_queue(check_list):
    for p in check_list:
        # check if the last_timestamp = None => passing to workers & start scraping
        if not p[1]:
            # publish_queue(p)      for redis channel connection
            create_worker(p)        # for create docker workers
        # else check if the from_account has new stuff to update?
        else:
            check_update(p)

        sleep(random.uniform(2.2, 5.6))


# Using redis to connect to workers
# to_scrap = (user_name, timestamp), type: Tuple
"""
def publish_queue(to_scrap):
    to_scrap = {"user_name": to_scrap[0], "last_time": to_scrap[1]}
    # redis publisher
    redis_connect.publish(
        const.REDIS_DB_CHANNEL,
        json.dumps(to_scrap)
    )
"""


# to_check = (user_name, timestamp), type: Tuple
def check_update(to_check):
    from_account = to_check[0]
    start_date = datetime.utcfromtimestamp(to_check[1]).strftime('%Y-%m-%d')

    driver = init_driver()
    fetch_search_page(driver=driver, start_date=start_date, from_account=from_account)

    if check_new_update(driver):
        create_worker(to_scrap=to_check)


# to_scrap = (user_name, timestamp), type: Tuple
def create_worker(to_scrap):

    from_account = to_scrap[0]

    # if last_timestamp = None => start scraping from last month
    if not to_scrap[1]:
        start_date = datetime.strftime(datetime.today() - relativedelta(months=1), '%Y-%m-%d')
    # else start scrap from last timestamp
    else:
        start_date = datetime.utcfromtimestamp(to_scrap[1]).strftime('%Y-%m-%d')

    # docker run --rm --name scrap_tester --network host worker_scrap:latest --from_account='@elonmusk' --start_date='2021-03-25'
    client.containers.run('worker_scrap', f'--from_account={from_account} --start_date={start_date}', stream=True,
                          detach=True, remove=True, network_mode='host')


if __name__ == '__main__':
    sleep(3)        # essential for waiting db image init

    # redis_connect = redis.Redis(host=const.REDIS_DB_HOST, port=const.REDIS_DB_PORT, db=const.REDIS_DB_NO, charset='utf-8', decode_responses=True)
    myCursor, myDB, from_accounts_list = init_db()

    # start the docker daemon from your host (already bind from the docker compose)
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    # docker build --no-cache -t worker_scrap .
    client.images.build(path='../worker-scraper/Dockerfile', nocache=True, tag='worker_scrap')

    while True:
        # latest_data = [(user_name: String, last_time_stamp: String), ...]
        latest_data = fetch_last_timestamp(from_accounts_list)
        render_queue(latest_data)
        sleep(random.uniform(10*60, 30*60))
