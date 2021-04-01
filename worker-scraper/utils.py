import json
import os
import random
import re
import const
from time import sleep

import chromedriver_autoinstaller
from googletrans import Translator
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def init_driver(proxy):
    chromedriver_path = chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    if const.APP_ENV != 'local':
        options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    if proxy:
        options.add_argument('--proxy-server=%s' % proxy)
    options.add_argument('log-level=3')
    driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    driver.set_page_load_timeout(100)
    return driver


def fetch_data(card):
    image_links = []
    try:
        username = card.find_element_by_xpath('.//span').text
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        postdate = int(datetime.timestamp(datetime.strptime(postdate, '%Y-%m-%dT%H:%M:%S.%fZ')))
    except:
        return

    text = "..."
    trans_text = translate_article(text)

    try:
        elements = card.find_elements_by_xpath('.//div[2]/div[2]//img[contains(@src, "https://pbs.twimg.com/")]')
        for element in elements:
            image_links.append(element.get_attribute('src'))
    except:
        image_links = []


    # get a string of all emojis contained in the tweet
    try:
        emoji_tags = card.find_elements_by_xpath('.//img[contains(@src, "emoji")]')
    except:
        return
    emoji_list = []
    for tag in emoji_tags:
        try:
            filename = tag.get_attribute('src')
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)

    # tweet url
    try:
        element = card.find_element_by_xpath('.//a[contains(@href, "/status/")]')
        post_url = element.get_attribute('href')
        tweet_id = post_url.rsplit('/', 1)[-1]
    except:
        return

    image_links = json.dumps(image_links)
    return tweet_id, username, handle, postdate, text, trans_text, emojis, image_links, post_url


def log_search_page(driver, start_date, end_date, from_account):
    from_account = "(from%3A" + from_account + ")%20" if from_account is not None else ""
    end_date = "until%3A" + end_date + "%20"
    start_date = "since%3A" + start_date + "%20"
    path = '...'

    driver.get(path)


def translate_article(text):
    try:
        translator = Translator()
        translation = translator.translate(text, src='en', dest='zh-tw')
        return translation.text
    except:
        return ''


def scrolling_down(driver, data, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position):

    while scrolling and tweet_parsed < limit:
        sleep(random.uniform(0.5, 1.5))
        # get the list of cards of tweets
        page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')

        for card in page_cards:
            tweet = fetch_data(card)
            if tweet:
                tweet_id = ''.join(tweet[0:3])
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)
                    tweet_parsed += 1
                    if tweet_parsed >= limit:
                        break

        scroll_attempt = 0
        while tweet_parsed < limit:
            # check scroll position
            sleep(random.uniform(1.3, 2.8))
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            scroll += 1
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 2:
                    scrolling = False
                    break
                else:
                    sleep(random.uniform(0.5, 1.5))  # attempt another scroll
            else:
                last_position = curr_position
                break
    return driver, data, tweet_ids, scrolling, tweet_parsed, scroll, last_position
