from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from time import sleep

def get_cookie():
    url = "https://login.taobao.com/"

    options = webdriver.ChromeOptions()

    options.add_experimental_option('excludeSwitches',['enable-automation'])

    driver = webdriver.Chrome(options=options)


    driver.get(url)


    username = driver.find_element_by_id('fm-login-id')
    password = driver.find_element_by_id('fm-login-password')
    username.send_keys('15625371430')
    sleep(2)
    password.send_keys('popo7758')
    sleep(2)
    submit_btn = driver.find_element_by_class_name('password-login')
    submit_btn.click()
    sleep(5)
    driver.switch_to_frame('baxia-dialog-content')
    sleep(2)
    sour = driver.find_element_by_id('nc_1_n1z')
    ele = driver.find_element_by_id('nc_1__scale_text')
    action = ActionChains(driver)
    action.click_and_hold(on_element=sour).perform()
    sleep(2)
    ActionChains(driver).move_to_element_with_offset(to_element=ele,xoffset=30,yoffset=0).perform()
    ActionChains(driver).move_to_element_with_offset(to_element=ele,xoffset=60,yoffset=0).perform()
    ActionChains(driver).move_to_element_with_offset(to_element=ele,xoffset=190,yoffset=0).perform()
    ActionChains(driver).move_to_element_with_offset(to_element=ele, xoffset=290, yoffset=0).perform()
    sleep(4)
    all_handle = driver.window_handles
    driver.switch_to_window(all_handle[0])
    sleep(2)
    submit_btn = driver.find_element_by_class_name('password-login')
    submit_btn.click()
    cookies = driver.get_cookies()
    # cookie_list = []
    # for item in cookies:
    #     cookie_list.append(item["name"] + "=" + item["value"])
    # cookie = ';'.join(cookie_list)
    cookie = {}
    cookies = driver.get_cookies()
    for item in cookies:
        cookie[str(item["name"])] = item["value"]
    sleep(5)
    return cookie



if __name__ == '__main__':
    print(get_cookie())
    # print({"cookie":get_cookie()})
