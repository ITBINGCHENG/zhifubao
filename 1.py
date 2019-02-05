from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import requests
import re
from selenium.webdriver.firefox.options import Options
#settings 内放置有全局变量
import settings
name = settings.name #支付宝张号与密码
password = settings.password

def browser():

    firefox_options =Options()
    firefox_options.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=firefox_options)
    #browser.set_window_size(240, 400)  # 参数数字为像素点
    return browser

def denglu(browser):

    try:
        driver = browser
        driver.maximize_window()
        driver.get('https://auth.alipay.com/login/index.htm?goto=https%3A%2F%2Fmy.alipay.com%2Fportal%2Fi.htm')
        # 等待2秒
        time.sleep(2)
        button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/ul/li[2]")
        button.click()
        time.sleep(2)
        #name = '………………@qq.com'
        driver.find_element_by_id('J-input-user').clear()
        driver.find_element_by_id('password_rsainput').clear()
        for x in name:
            driver.find_element_by_id('J-input-user').send_keys(x)
            time.sleep(0.5)
        time.sleep(3)
        #password = "***"
        for x in password:
            driver.find_element_by_id('password_rsainput').send_keys(x)
            time.sleep(0.5)
        time.sleep(2)
        driver.find_element_by_id('J-login-btn').click()
        time.sleep(2)
        # 获取cookie，并保存到本地
        cookies = driver.get_cookies()
        with open('cookies', 'w') as f:
            json.dump(cookies, f)
        f.close()
        #driver.close()
    except:
        print('登录错误')
        denglu(browser)


# 判断是否已经登录



def get_data(browser):
    driver = browser
    #button = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[2]/div[4]")
    #print(button)#用来定义采集的订单范围
    time.sleep(2)
    #button.click()
    time.sleep(2)
    # for i in range(1,21):
    #     element = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[4]/div[2]/div/div/div/div/div/div[1]/div/table/tbody/tr["+str(i)+"]/td[2]/span/span").text
    #     print(element)#所要采集的元素
    #

    element = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div[1]/button/div[1]/span[2]").text
    print(element)

if __name__ == "__main__":
    browser=browser()
    denglu(browser)
    i = 0
    browser.get("https://mbillexprod.alipay.com/enterprise/tradeListQuery.htm")  # 采集页面
    while True:
        try:
            i=i+1

            get_data(browser)
            time.sleep(30)#30秒采集一次
            browser.refresh()
            print(i)

        except:
            browser.close()
            browser = browser()
            denglu(browser)
            browser.get("https://mbillexprod.alipay.com/enterprise/tradeListQuery.htm")  # 采集页面\
            i = 0
            continue

#denglu(browser)

#quickTimeItem___r5kmW active___PXMMa