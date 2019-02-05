# -*- coding=utf-8 -*-
from selenium import webdriver
import time
import json
import requests
from lxml import etree
import pymysql


class AlipaySpider(object):

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}
        self.session = requests.Session()
        self.session.headers = self.headers
        self.number_list = []
        self.time_list = []
        self.content_list = []
        self.money_list = []
        self.state_list = []

    # 用webdriver 获取cookie
    def save_cookies(self):
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get('https://auth.alipay.com/login/index.htm?goto=https%3A%2F%2Fmy.alipay.com%2Fportal%2Fi.htm')
        # 等待2秒
        time.sleep(2)
        button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/ul/li[2]")
        button.click()
        time.sleep(2)
        name = '##@qq.com'
        for x in name:
            driver.find_element_by_id('J-input-user').send_keys(x)
            time.sleep(0.5)
        time.sleep(3)
        password = "￥￥￥"
        for x in password:
            driver.find_element_by_id('password_rsainput').send_keys(x)
            time.sleep(0.5)
        time.sleep(2)
        driver.find_element_by_id('J-login-btn').click()
        # 获取cookie，并保存到本地
        cookies = driver.get_cookies()
        with open('cookies','w') as f:
            json.dump(cookies, f)
        f.close()
        driver.close()

    # 设置cookie
    def set_cookies(self):
    # 从文件中获取cookie
        with open('cookies', 'r') as f:
            cookies = json.load(f)
        # 将json存储的cookie 转化为dict，并更新session的coookie
        for cookie in cookies:
            c = {cookie['name']: cookie['value']}
            self.session.cookies.update(c)

    # 判断是否已经登录
    def aready_login(self):
        self.set_cookies()
        html_code = self.session.get('https://custweb.alipay.com/account/index.htm',allow_redirects=False).status_code
        if html_code == 200:
            return True
        else:
            return False

    # 获取数据
    def get_data(self):
        # 获取交易记录界面
        html = self.session.get('https://consumeprod.alipay.com/record/standard.htm')
        # 用lxml解析html
        selector= etree.HTML(html.text)
        print(html.text)
        # 获取最近20个交易数据
        for i in range(1,21):
            # 获取流水号
            number = selector.xpath('//*[@id="J-tradeNo-'+str(i)+'"]/@title')
            self.number_list.append(number[0].strip())
            # 获取交易时间
            time = selector.xpath('//*[@id="J-item-'+str(i)+'"]/td[2]/p[1]/text()')
            self.time_list.append(time[0].strip())
            # 获取具体内容
            try:
                # 交易成功的内容
                content = selector.xpath('//*[@id="J-item-'+str(i)+'"]/td[3]/p[1]/a/text()')
                self.content_list.append(content[0].strip())
            except:
                # 交易失败的内容
                content = selector.xpath('//*[@id="J-item-'+str(i)+'"]/td[3]/p[1]/text()')
                self.content_list.append(content[0].strip())
            # 获取金额变动
            money = selector.xpath('//*[@id="J-item-'+str(i)+'"]/td[4]/span/text()')
            self.money_list.append(money[0].strip())
            # 获取交易状态
            state = selector.xpath('//*[@id="J-item-'+str(i)+'"]/td[6]/p[1]/text()')
            self.state_list.append(state[0].strip())

    # 存储数据
    def save_data(self):
        # 连接数据库
        db = pymysql.connect('localhost', 'root', '123456', 'test1')
        # 获取游标
        cursor = db.cursor()
        for i in range(20):
            # sql 插入语句，插入到alipay表中
            sql = "INSERT IGNORE INTO alipay(NUMBER,DATE,CONTENT,MONEY,STATE) VALUES ('%s','%s','%s','%s','%s')" % (self.number_list[i],self.time_list[i],self.content_list[i],self.money_list[i],self.state_list[i])
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库
                db.commit()
            except:
                # 失败回滚
                db.rollback()
        # 关闭数据库连接
        db.close()

    def total_crawl(self):
        self.save_cookies() # 保存cookie
        self.set_cookies() # 设置cookie
        self.get_data() # 爬取数据
        self.save_data() # 保存数据

    def crawl(self):
        self.get_data() # 爬取数据
        self.save_data() # 保存数据

if __name__ == "__main__":
    spider = AlipaySpider()
    if spider.aready_login() == True:
        spider.crawl()
    else:
        spider.total_crawl()