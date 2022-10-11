import settings
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import time
import random as rand

import os
import shutil

MAGIC_RED_THRETHOLD = 150

def wait_until_complete(driver):
    WebDriverWait(driver, 500).until(lambda x: driver.execute_script('return document.readyState == "complete"'))

def load_and_scroll_to_end(driver):
    while True:
        height = driver.execute_script("return action=document.body.scrollHeight")
        init_time = time.time()

        while time.time() - init_time < 10:
            driver.execute_script('window.scrollTo(0, 0)')
            time.sleep(.2)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(.2)
            

        if height == driver.execute_script("return action=document.body.scrollHeight"):
            break

def checked(item):
    button = item.find_element(by=By.XPATH, value="./uni-view[5]")
    color_string = button.value_of_css_property("color")
    red = int(re.search("rgb\((\d*)[,\s]", color_string).groups()[0])

    return red < MAGIC_RED_THRETHOLD

def check_in(student_id, student_name, driver):
    path = "login_coords/{}{}".format(student_id, student_name)
    if not os.path.exists(path):
        os.makedirs(path)
        shutil.copy("default_coord", "{}/coord".format(path))


    with open("{}/coord".format(path)) as file:
        text = file.readline().replace('\n', '')
        coord = file.readline().replace('\n', '')


        post_string = """[{\\"question_id\\":48,\\"answer\\":{\\"id\\":111,\\"text\\":null}},{\\"question_id\\":36,\\"answer\\":{\\"id\\":71,\\"text\\":\\\"""" + text + """\\",\\"location\\":\\\"""" + coord + """\\"}},{\\"question_id\\":50,\\"answer\\":{\\"id\\":114,\\"text\\":null}},{\\"question_id\\":51,\\"answer\\":{\\"id\\":118,\\"text\\":null}},{\\"question_id\\":52,\\"answer\\":{\\"id\\":121,\\"text\\":null}},{\\"question_id\\":54,\\"answer\\":{\\"id\\":126,\\"text\\":null}},{\\"question_id\\":56,\\"answer\\":{\\"id\\":130,\\"text\\":null}},{\\"question_id\\":58,\\"answer\\":{\\"id\\":134,\\"text\\":null}},{\\"question_id\\":60,\\"answer\\":{\\"id\\":137,\\"text\\":null}},{\\"question_id\\":64,\\"answer\\":{\\"id\\":145,\\"text\\":null}},{\\"question_id\\":65,\\"answer\\":{\\"id\\":149,\\"text\\":null}},{\\"question_id\\":67,\\"answer\\":{\\"id\\":152,\\"text\\":null}},{\\"question_id\\":93,\\"answer\\":{\\"id\\":240,\\"text\\":null}},{\\"question_id\\":94,\\"answer\\":{\\"id\\":244,\\"text\\":null}},{\\"question_id\\":75,\\"answer\\":{\\"id\\":184,\\"text\\":null}},{\\"question_id\\":95,\\"answer\\":{\\"id\\":252,\\"text\\":null}}]"""
        wait_until_complete(driver)
        WebDriverWait(driver, 500).until(lambda x: driver.execute_script("return typeof uni !== 'undefined'"))
        print("uni loaded")
        time.sleep(5)
        script = """
        var xhr = new XMLHttpRequest();
        args = /\?(.*)/.exec(window.location.href)[1];
        xhr.open("POST", "https://yqfk.bjut.edu.cn/api/home/butian/daily_store?" + args);
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
        print("{} done".format(student_name))
    
    driver.back()


driver = webdriver.Firefox()

driver.get("""https://cas.bjut.edu.cn/login?service=https%3A%2F%2Fitsapp.bjut.edu.cn%2Fa_bjut%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fitsapp.bjut.edu.cn%252Fuc%252Fapi%252Foauth%252Findex%253Fredirect%253Dhttp%253A%252F%252Fyqfk.bjut.edu.cn%252Fapi%252Flogin%252Fpages-report-index%253Flogin%253D1%2526appid%253D200220501233430304%2526state%253DSTATE%26from%3Dwap""")
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
time.sleep(5)
load_and_scroll_to_end(driver)
wait_until_complete(driver)
time.sleep(5)
print("idk loaded")

done_list = []

while True:
    load_and_scroll_to_end(driver)
    items_in_lists = driver.find_elements(by=By.CLASS_NAME, value="content-list")


    filtered = filter(lambda it: not checked(it), items_in_lists)
    filtered = list(filter(lambda it: done_list.count(it.text) == 0, filtered))
    
    item = None

    if (len(filtered) == 0):
        break
    else:
        item = filtered[0]
        done_list.append(item.text)

    student_id = item.find_element(by=By.XPATH, value="./uni-view[2]").text
    student_name = item.find_element(by=By.XPATH, value="./uni-view[1]").text
    button = item.find_element(by=By.XPATH, value="./uni-view[5]")

    button.click()
    wait_until_complete(driver)


    check_in(student_id, student_name, driver)

driver.close()
