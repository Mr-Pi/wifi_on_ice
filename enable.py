#!/usr/bin/env python3
import argparse
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep


parser = argparse.ArgumentParser(description='Enables unlimited WiFi Data at the Deutsch Bahn ICE WiFi network')
parser.add_argument('-I', '--interface', type=str, help='defines the wlan interface to use', default='wlan0')
parser.add_argument('--firefox-options', type=str, help='additional arguments to parse to firefox', default=['--headless'], nargs=argparse.REMAINDER)
args = parser.parse_args()

firefox_options=Options()
for option in args.firefox_options:
    firefox_options.add_argument(option)

while True:
    driver = webdriver.Firefox(firefox_options=firefox_options)
    driver.get('http://login.wifionice.de/de/')
    try:
        sleep(2)
        quota_now = driver.find_element(By.CLASS_NAME, 'progress-bar').get_attribute('aria-valuenow')
        print('Currently {}% of your quota are used.'.format(quota_now))
        if int(quota_now) > 90:
            print('More than 90% of your quota are used, reconnecting!!!')
            os.system('sudo ip l set {} down'.format(args.interface))
            os.system('sudo macchanger -e {}'.format(args.interface))
            os.system('sudo ip l set {} up'.format(args.interface))
    except NoSuchElementException:
        driver.find_element(By.ID, 'connect').submit()
        continue
    driver.quit()
    os.system('sudo true')  # keep sudo active
    sleep(30)
