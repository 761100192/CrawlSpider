from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from time import sleep

url = "https://passport.ctrip.com/user/member/fastOrder"


options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches',['enable-automation'])

driver = webdriver.Chrome(options=options)


driver.maximize_window()


driver.get(url)

sleep(5)


phone = driver.find_element_by_id('txt_phone')
phone.send_keys("15625371430")

sleep(2)


sour = driver.find_element_by_class_name('cpt-drop-btn')
ele = driver.find_element_by_class_name('cpt-bg-bar')

action = ActionChains(driver)
action.click_and_hold(on_element=sour).perform()
print(sour.size)
print(ele.size,ele.location['x'])
# sleep(0.15)
action.move_by_offset(30,0).perform()
sleep(0.5)
action.move_by_offset(100,0).perform()
sleep(0.5)
action.move_by_offset(190,0).perform()
sleep(0.5)
# ActionChains(driver).move_to_element_with_offset(to_element=sour,xoffset=30,yoffset=0).perform()
# sleep(0.5)
# ActionChains(driver).move_to_element_with_offset(to_element=sour,xoffset=100,yoffset=0).perform()
# sleep(0.5)
# ActionChains(driver).move_to_element_with_offset(to_element=sour,xoffset=190,yoffset=0).perform()
# ActionChains(driver).move_by_offset(30,0)
# sleep(0.5)
# ActionChains(driver).move_by_offset(60,0)
# sleep(0.5)
# ActionChains(driver).move_by_offset(190,0)
action.release()
print(190,sour.location['x'],sour.location['y'] )
sleep(4)
# btn_getCode = driver.find_element_by_id('btn_getCode')
# btn_getCode.click()
cookie = ""
cookie_list = []
# print(driver.get_cookies())
for item in driver.get_cookies():
    cookie_list.append(item["name"] + "=" + item["value"])

print(driver.get_cookies())
cookie = ';'.join(cookie_list)
print(cookie)
print(driver.get_cookie("_ga"))
