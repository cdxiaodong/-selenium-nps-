# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import wmi
import os
import threadpool


start = time.time()
c = wmi.WMI ()
for process in c.Win32_Process (name="chromedriver.exe"):
    print(process.ProcessId, process.Name)
    process.Terminate()
chrome_options = Options()
#chrome_options.add_argument('headless')# 浏览器不提供可视化页面（无头模式）. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--disable-gpu') #如果不加这个选项，有时定位会出现问题
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disk-cache=no')  # 开启缓存（可选）
chrome_options.add_argument('--ignore-ssl-errors=true')  # 忽略https错误(可选)
chrome_options.add_argument('--start-maximized')  # 启动Google Chrome就最大化
chrome_options.add_argument('--user-agent="{}"'.format(Automated().uarand()))  # 修改HTTP请求头部的Agent字符串，可以通过about:version页面查看修改效果
chrome_options.add_argument('--incognito')  # 启动进入隐身模式
chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 完美去除window.navigator.webdriver
chrome_options.add_argument('--disable-infobars')  # 关闭自动化提示框
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])  # 忽略 DevTools listening on ws://127.0.0.1... 提示

bo = webdriver.Chrome(chrome_options=chrome_options,executable_path='D:\\1\\chrome\\chromedriver.exe')


bo.implicitly_wait(10)#隐式等待10s

bo.set_page_load_timeout(10)  #没设置这两个set的话异常在xpath那边(也就是获取js)  设置了这个的话 异常在get(url)这边
bo.set_script_timeout(10)#这两种设置都进行才有效


for url in open("urls.txt"):
    try:
        bo.get(url)  #driver.get(url)方法可以跳转到要访问的网页去
    except :
        continue
    
    wait = WebDriverWait(bo, 3)#显式等待，用一个默认频率不停的刷新（默认是0.5s），检测当前页面元素是否存在，如果超过10秒则抛出TimeOut。
    
    #input_account = bo.find_element(By.XPATH,//*[@placeholder="用户名"])   可
    try:
        input_account = bo.find_element(By.XPATH,value="//*[@name='username']")
    except :
        continue
    #input_account = bo.find_element(By.NAME,'username')   可
    input_account.send_keys('admin') #使用固定用户admin
    input_password = bo.find_element(By.XPATH,value="//*[@name='password']")
    input_password.send_keys('123')   #使用固定密码123
    login_button = bo.find_element(By.XPATH,value="//*[@onclick='login()']")     #模拟点击登录按钮
    login_button.click()
    # print(url)
    #**先利用方法switch_to_alert()定位到alert等弹出框，再进行相应的处理(确认、取消、输入值)**
    time.sleep(0.3) #等待结果
    # alter = bo.switch_to.alert
    # alter.text
    #判断是否有弹窗
    

    result = EC.alert_is_present()(bo)
    if result:
        print("%swudong" %url)
        result.accept()
    else:
        print("%s有洞" %url)

    
    url = url.strip('\n')
    
bo.close()    
    
    
end = time.time()
print("耗时" + str(end-start))