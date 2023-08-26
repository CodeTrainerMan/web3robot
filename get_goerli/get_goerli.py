# //a8f286dad429323ea9366e04c67bc1d7

import requests, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys


# ads_id = "j4px73q"


# resp = requests.get(open_url).json()
# if resp["code"] != 0:
#     print(resp["msg"])
#     print("please check ads_id")
#     sys.exit()
#
# chrome_driver = resp["data"]["webdriver"]
# chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
# driver = webdriver.Chrome(chrome_driver, options=chrome_options)
# print(driver.title)
# driver.get("https://www.baidu.com")
# time.sleep(5)
# driver.quit()
# requests.get(close_url)


def load_data():
    accounts = ["0xA76f2B935C04Ab0D1c2EB16a4A7f410C656Cf645", "0x81cD2B890971AE4920943C601E53867EfCA0BFf7",
                "0xaa44b72D7c3F2E5963745B78c8Fbb04de26C67b8", "0x2e01d85B648E8ba05dB3CCD6C7d6944b2394382e",
                "0x00d69Ab6b9ca27aB93E4DA6F299FD0D6236B1237", "0xc9De3E02864b177D43426f64fB23cED212d7F5FE",
                "0x99c0F0409B2b8D02CCBbB7792dbea64dc9d8198C", "0x28c7694A4fc7e51db403b2A260a6882c0839f883",
                "0xC85f9f8413FB909142b79Efc313dC49CD453C608", "0x0b415e4F0a59e76324707727Ec20233737e844B5",
                "0x0b415e4F0a59e76324707727Ec20233737e844B5",
                ]
    ads_id = ["j4powkl", "j4powkm",
              "j4powkn", "j4powko",
              "j4powkq", "j4powkr",
              "j4powks", "j4powkt",
              "j4powku", "j4powkv",
              "j4px73h",
              ]

    return accounts, ads_id


def get_driver(url):
    resp = requests.get(url).json()
    if resp["code"] != 0:
        print(resp["msg"])
        print("please check ads_id")
        sys.exit()

    chrome_driver = resp["data"]["webdriver"]
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)
    return driver


if __name__ == '__main__':
    webdriver = None
    open_url = "http://127.0.0.1:50325/api/v1/browser/start?user_id="
    close_url = "http://127.0.0.1:50325/api/v1/browser/stop?user_id="
    try:
        accounts, ads_id = load_data()
        j = 0

        for i in range(accounts):
            open_url = open_url + accounts[i]
            close_url = close_url + accounts[i]
            webdriver = get_driver(open_url)
            webdriver.get("https://www.baidu.com")

            if (len(ads_id) < len(accounts)) and (j == len(ads_id)):
                j = 0
            else:
                j = j + 1
            webdriver.quit()
            requests.get(close_url)

    except Exception as e:

        if webdriver is not None:
            webdriver.quit()
            requests.get(close_url)
        print("运行报错:" + e)
