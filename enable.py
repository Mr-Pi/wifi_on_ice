#!/usr/bin/env python3
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

firefox_options=Options()
firefox_options.add_argument("--headless")
while True:
    driver = webdriver.Firefox(firefox_options=firefox_options)
    driver.get("http://login.wifionice.de/de/")
    try:
        quota_now = driver.find_element(By.CLASS_NAME, "progress-bar").get_attribute("aria-valuenow")
        print("Currently {}% of your quota are used.".format(quota_now))
        if int(quota_now) > 90:
            print("More than 90% of your quota are used, reconnecting!!!")
            os.system("sudo ip l set wlan0 down")
            os.system("sudo macchanger -e wlan0")
            os.system("sudo ip l set wlan0 up")
    except NoSuchElementException:
        driver.find_element(By.ID, "connect").submit()
        continue
    driver.quit()
    os.system("sudo true")  # keep sudo active
    time.sleep(30)
