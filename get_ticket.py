#!/usr/bin/python
#coding:utf-8
# chrome驱动：http://chromedriver.storage.googleapis.com/index.html
# 驱动放在 C:/Windows/System32

import threading
from subprocess import Popen,PIPE
from splinter.browser import Browser
from time import sleep
import sys

username = "xxxxxx"
passwd = "xxxxxx"

fromStation = "%u5317%u4EAC%2CBJP"
toStation = "%u798F%u5DDE%2CFZS"
dtime = "2016-12-20"

train_num = 2  #0表示从上到下依次点击预定
#urls
login_url = "https://kyfw.12306.cn/otn/login/init"
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"

def login():
    b.find_by_text(u"登录").click()
    b.fill("loginUserDTO.user_name",username)
    b.fill("userDTO.password",passwd)
    sleep(13)

def get_click():
    while b.url == ticket_url:          
        if b.find_by_text(u"预订"):
            b.find_by_text(u"预订")[train_num - 1].click()

def get_click_choosen():
    if train_num != 0:
        while b.url == ticket_url:          
            if b.find_by_text(u"预订"):
                b.find_by_text(u"预订")[train_num - 1].click()
    else:
        while b.url == ticket_url:
            if b.find_by_text(u"预订"):
                for i in b.find_by_text(u"预订"):
                    i.click()

def main():
    global b
    b = Browser(driver_name="chrome")
    b.visit(ticket_url)
    while b.is_text_present(u"登录"):
        sleep(1)
        login()
        try:
            b.visit(ticket_url)
            b.cookies.add({"_jc_save_fromStation":fromStation})
            b.cookies.add({"_jc_save_toStation":toStation})
            b.cookies.add({"_jc_save_fromDate":dtime})
            b.reload()
            b.find_by_text(u"查询").click();sleep(2)
            b.find_by_text(u"学生").click()    #选择学生票
 
            threads = []
            thread_count = 10
            for i in range(thread_count):
                t = threading.Thread(target=get_click,args=())
                threads.append(t)
            for i in range(thread_count):
                threads[i].start()
            for i in range(thread_count):
                threads[i].join()

        except Exception, e:
            b.execute_script('alert("Something wrong...")')
            b.get_alert().dismiss()
        else:
            pass
        finally:
            pass
if __name__ == '__main__':
    main()