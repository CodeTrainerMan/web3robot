# //a8f286dad429323ea9366e04c67bc1d7

import requests,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

ads_id = "j4px73q"
open_url = "http://127.0.0.1:50325/api/v1/browser/start?user_id=" + ads_id
close_url = "http://127.0.0.1:50325/api/v1/browser/stop?user_id=" + ads_id

resp = requests.get(open_url).json()
if resp["code"] != 0:
    print(resp["msg"])
    print("please check ads_id")
    sys.exit()

chrome_driver = resp["data"]["webdriver"]
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
driver = webdriver.Chrome(chrome_driver, options=chrome_options)
print(driver.title)
driver.get("https://www.baidu.com")
time.sleep(5)
driver.quit()
requests.get(close_url)