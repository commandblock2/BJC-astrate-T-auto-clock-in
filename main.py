import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import time
import random as rand

import logging
import sys

def wait_until_complete(driver):
    WebDriverWait(driver, 500).until(lambda x: driver.execute_script('return document.readyState == "complete"'))

logger = logging.getLogger('logfuck')
sys.excepthook = lambda t, v, tb: logger.exception(str(v))

driver = webdriver.Firefox()

driver.get("https://itsapp.bjut.edu.cn/uc/wap/login?redirect=https://itsapp.bjut.edu.cn/site/applicationSquare/index?sid=2")
driver.maximize_window()
driver.switch_to.frame("loginIframe")
with open("login") as file:
    (username, password) = file.readline().split(" ")
    wait_until_complete(driver)
    print("login loaded")
    driver.find_element(value="unPassword").send_keys(username)
    driver.find_element(value="pwPassword").send_keys(password)

driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/div[7]/input").click()


driver.switch_to.parent_frame()
wait_until_complete(driver)
print("idk loaded")
time.sleep(5)
driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[1]/div/section/div/div[3]/div[1]/ul/li[2]").click()

with open("coord") as file:
    text = file.readline().replace('\n', '')
    coord = file.readline().replace('\n', '')

    post_string = """[{\\"question_id\\":48,\\"answer\\":{\\"id\\":111,\\"text\\":null}},{\\"question_id\\":36,\\"answer\\":{\\"id\\":71,\\"text\\":\\\"""" + text + """\\",\\"location\\":\\\"""" + coord + """\\"}},{\\"question_id\\":50,\\"answer\\":{\\"id\\":114,\\"text\\":null}},{\\"question_id\\":51,\\"answer\\":{\\"id\\":118,\\"text\\":null}},{\\"question_id\\":52,\\"answer\\":{\\"id\\":121,\\"text\\":null}},{\\"question_id\\":54,\\"answer\\":{\\"id\\":126,\\"text\\":null}},{\\"question_id\\":56,\\"answer\\":{\\"id\\":130,\\"text\\":null}},{\\"question_id\\":58,\\"answer\\":{\\"id\\":134,\\"text\\":null}},{\\"question_id\\":60,\\"answer\\":{\\"id\\":137,\\"text\\":null}},{\\"question_id\\":64,\\"answer\\":{\\"id\\":145,\\"text\\":null}},{\\"question_id\\":65,\\"answer\\":{\\"id\\":149,\\"text\\":null}},{\\"question_id\\":67,\\"answer\\":{\\"id\\":152,\\"text\\":null}},{\\"question_id\\":93,\\"answer\\":{\\"id\\":240,\\"text\\":null}},{\\"question_id\\":94,\\"answer\\":{\\"id\\":244,\\"text\\":null}},{\\"question_id\\":75,\\"answer\\":{\\"id\\":184,\\"text\\":null}},{\\"question_id\\":95,\\"answer\\":{\\"id\\":252,\\"text\\":null}}]"""

    wait_until_complete(driver)
    WebDriverWait(driver, 500).until(lambda x: driver.execute_script("return typeof uni !== 'undefined'"))
    print("uni loaded")
    time.sleep(5)
    script = """
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "https://yqfk.bjut.edu.cn/api/home/daily_form");

    bearer = uni.getStorageSync('token');
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", "Bearer " + bearer);
    xhr.send("{}");
    xhr.onerror = console.log;
    xhr.onload = console.log;
    console.log(xhr.responseText);
    return xhr.responseText;
    """.format(post_string).replace('\n', '')
    print(driver.execute_script(script))

#driver.close()
