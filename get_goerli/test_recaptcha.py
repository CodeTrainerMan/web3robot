
#
# from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import os, sys
import time, requests
from bs4 import BeautifulSoup
import aliNls

delayTime = 2
audioToTextDelay = 10
filename = '1.mp3'
byPassUrl = 'https://mumbaifaucet.com/'
googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'
option = uc.ChromeOptions()
option.add_argument('--no-sandbox')
# option.add_argument('--disable-notifications')
# option.add_argument("--mute-audio")
# 禁用浏览器提示正在受自动化软件控制
# option.add_experimental_option('useAutomationExtension', False)
# 防止反爬
# option.add_experimental_option('excludeSwitches', ['enable-automation'])
# 谷歌文档提到需要加上这个属性来规避bug
option.add_argument('--disable-gpu')

option.add_argument('--user-data-dir=D:\\Program Files (x86)\\Google\\Chrome\\Application\\User Data')
# 指定缓存Cache路径
option.add_argument('--disk-cache-dir=D:\\Program Files (x86)\\Google\\Chrome\\Application\\User Data')
# option.add_argument('--proxy-server=http://127.0.0.1:10809')
# option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
option.add_argument(
    "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")

option.add_argument('--disable-dev-shm-usage')
option.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"



def saveFile(content, filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)
def pass_recaptcha():
    flag = False
    outeriframe = driver.find_elements(By.XPATH, "//*[@title='reCAPTCHA']")
    if len(outeriframe)>0:
        outeriframe = outeriframe[0]
    else:
        return True
    time.sleep(1)
    outeriframe.click()
    time.sleep(2)
    allIframesLen = driver.find_elements(By.TAG_NAME, 'iframe')
    time.sleep(1)
    audioBtnFound = False
    audioBtnIndex = -1
    for index in range(len(allIframesLen)):
        driver.switch_to.default_content()
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element(By.ID, 'recaptcha-audio-button') or driver.find_element(By.ID,
                                                                                                   'recaptcha-anchor')
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass
    if audioBtnFound:
        need_help = driver.find_elements(By.LINK_TEXT, "我们的帮助页面")
        if len(need_help)>0:
            return False
        try:
            while True:
                href = driver.find_element(By.ID, 'audio-source').get_attribute('src')
                response = requests.get(href, stream=True)
                saveFile(response, filename)
                response = aliNls.AliNLS().get_str_from_voice(audio_file=filename)
                print(response)
                driver.switch_to.default_content()
                iframe = driver.find_elements(By.TAG_NAME, 'iframe')[audioBtnIndex]
                driver.switch_to.frame(iframe)
                inputbtn = driver.find_element(By.ID, 'audio-response')
                inputbtn.send_keys(response)
                inputbtn.send_keys(Keys.ENTER)
                time.sleep(2)
                errorMsg = driver.find_elements(By.CLASS_NAME, 'rc-audiochallenge-error-message')[0]
                if errorMsg.text == "" or errorMsg.value_of_css_property('display') == 'none':
                    print("Success")
                    return audioBtnFound
                break
        except Exception as e:

            print(e)
            print('Caught. Need to change proxy now')
            return audioBtnFound
    else:
        print('Button not found. This should not happen.')
        return audioBtnFound

driver = uc.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options=option)


accounts = [
            "0xaa44b72D7c3F2E5963745B78c8Fbb04de26C67b8", "0x2e01d85B648E8ba05dB3CCD6C7d6944b2394382e",
            "0x00d69Ab6b9ca27aB93E4DA6F299FD0D6236B1237", "0xc9De3E02864b177D43426f64fB23cED212d7F5FE",
            "0x99c0F0409B2b8D02CCBbB7792dbea64dc9d8198C", "0x28c7694A4fc7e51db403b2A260a6882c0839f883",
            "0xC85f9f8413FB909142b79Efc313dC49CD453C608", "0x0b415e4F0a59e76324707727Ec20233737e844B5",
            "0x0b415e4F0a59e76324707727Ec20233737e844B5",
            ]
for i in accounts:
    driver.get(byPassUrl)
    driver.refresh()
    time.sleep(1)
    #
    # while (pass_recaptcha()==False):
    #     driver.quit()
    #     driver = uc.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
    #                               options=option)
    #     driver.get(byPassUrl)
    #     time.sleep(1)
    driver.switch_to.default_content()
    time.sleep(1)
    inputbtn = driver.find_element(By.XPATH, '//form/div/div[1]/input')
    inputbtn.send_keys(i)
    time.sleep(2)
    outeriframe = driver.find_element(By.XPATH, "//form/div/div[2]/button")
    time.sleep(1)
    outeriframe.click()
    time.sleep(15)


