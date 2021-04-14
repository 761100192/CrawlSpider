import csv
import requests
from lxml import etree
from bs4 import  BeautifulSoup
import time
import os
from random import choice



class lagou():

    def __init__(self):
        self.headers = {
            "Cookie":"__lg_stoken__=4b2560ea54bf34409f7e018129ce9ead404d3c5a03c639cdd2417fb2033582183b66f1d53287e1e15a42f0066b63d4826da611f2696a5ff6100613a236136ff5194477e5c6b1;"
            ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
        self.proxy_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Cookie": "UM_distinctid=1788b7c2934abe-093bcfa114abfe-5771031-fa000-1788b7c2935b21; Hm_lvt_2ace778af27f12fd56d10f936c428deb=1617251532,1617257966,1617267513,1617351051; Hm_lpvt_2ace778af27f12fd56d10f936c428deb=1617351860"
        }
        filename = "lagou-" + time.strftime("%Y-%m-%d") + ".csv"
        self.fp = open(filename,"w",encoding="utf-8",newline="")


    def get_proxy_ip(self):

        response = requests.get("http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=b408feba0db2062c37bc4a11fc774f0a&orderNo=GL20210401113444SD8q5Ujx&count=5&isTxt=0&proxyType=1",
                                headers=self.proxy_headers).json()
        ip_list = []
        for item in response["obj"]:
            ip_list.append(item["ip"] + item["port"])
        ip = choice(ip_list)
        self.change_proxy_ip(ip)
        return ip



    def change_proxy_ip(self,ip):
        response = requests.get("http://www.xiongmaodaili.com/xiongmao-web/clientWhilteList/listUserIp?secret=b408feba0db2062c37bc4a11fc774f0a",
                     headers=self.proxy_headers).json()
        ip_list = []
        for item in response["obj"]:
            ip_list.append(item["ip"])
        old_ip = choice(ip_list)
        url = "http://www.xiongmaodaili.com/xiongmao-web/whilteList/addOrUpdate?orderNo=GL20210401113444SD8q5Ujx&secret=b408feba0db2062c37bc4a11fc774f0a&oldIp={old_ip}&newIp={ip}"\
            .format(old_ip=old_ip,ip=ip)
        response = requests.get(url,headers=self.proxy_headers).json()


    def parse_page(self):
        pass




if __name__ == '__main__':
    pass









if __name__ == '__main__':
    pass