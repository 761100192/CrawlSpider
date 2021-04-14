from selenium import webdriver
import time

desire_caps = {}

desire_caps["platformName"]="Android"
desire_caps["platformVersion"]="6.0"
desire_caps["deviceName"]="HuaWeiP9"
desire_caps["appPackage"]="com.taobao.taobao"
desire_caps["appActivity"]="com.taobao.tao.homepage.MainActivity3"
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",desire_caps)
driver.find_element_by_id("com.taobao.taobao:id/home_searchedit").click()
time.sleep(3)
driver.find_element_by_id("com.taobao.taobao:id/searchEdit").send_keys("adidas")
driver.find_element_by_id("com.taobao.taobao:id/searchbtn").click()
