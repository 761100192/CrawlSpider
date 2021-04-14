from lxml import etree
from bs4 import BeautifulSoup
import requests
import csv
import time
from random import choice

class douban:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
        self.proxy_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Cookie": "UM_distinctid=1788b7c2934abe-093bcfa114abfe-5771031-fa000-1788b7c2935b21; Hm_lvt_2ace778af27f12fd56d10f936c428deb=1617251532,1617257966,1617267513,1617351051; Hm_lpvt_2ace778af27f12fd56d10f936c428deb=1617351860"
        }
        filename = "douban-" + time.strftime("%Y-%m-%d",time.localtime()) + ".csv"
        self.fp = open(filename,"w",encoding="utf-8",newline="")
        self.csver = csv.writer(self.fp)
        self.csver.writerow(["book_name","author","publish",
                             "publish_author","translator","page",
                             "price","decoration","ISBN","average_rate"])


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

    def write_to_csv(self,item):
        data = [item["book_name"],item["author"],item["publish"],
                item["publish_author"],item["translator"],item["page"],
                item["price"],item["decoration"],item["ISBN"],item["average_rate"]]
        self.csver.writerow(data)


    def parse_page(self):
        urls = []
        ip = self.get_proxy_ip()
        proxys = {
            "http":"http://" + ip
        }
        for page in range(0,21):
            url = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={page}&type=T".format(page= page * 20)
            print("正在爬取搜索页:{url}".format(url=url))
            response = requests.get(url=url,headers=self.headers,proxies=proxys).text
            page = BeautifulSoup(response,"html.parser")
            flag = page.find_all("input",attrs={"name":"captcha-solution"})
            if len(flag) != 0:
                ip = self.get_proxy_ip()
                proxys = {
                    "http": "http://" + ip
                }
                response = requests.get(url=url, headers=self.headers, proxies=proxys).text
            tree = etree.HTML(response)
            li_list = tree.xpath('//ul[@class="subject-list"]/li')
            for li in li_list:
                url_ = li.xpath('./div[@class="info"]/h2/a/@href')[0]
                urls.append(url_)
            time.sleep(2)
        return urls


    def parse(self,urls):
        ip = self.get_proxy_ip()
        proxys = {
            "http": "http://" + ip
        }
        for item in urls:
            print("正在爬取详情页:{url}".format(url=item))
            response = requests.get(url=item, headers=self.headers, proxies=proxys).text
            page = BeautifulSoup(response, "html.parser")
            flag = page.find_all("input", attrs={"name": "captcha-solution"})
            if len(flag) != 0:
                ip = self.get_proxy_ip()
                proxys = {
                    "http": "http://" + ip
                }
                response = requests.get(url=item, headers=self.headers, proxies=proxys).text
            self.parse_detail(response)
            time.sleep(2)





    def parse_detail(self,response):
        tree = etree.HTML(response)
        data = {}
        publish = tree.xpath('//div[@id="info"]/span[@class="pl"][contains(text(),"出版社:")]/following::text()[1] | //div[@id="info"]/span[@class="pl"][contains(text(),"出版社:")]/following::text()[2]')
        publish = self.judge_num(publish)
        publish_author = tree.xpath('//div[@id="info"]//span[@class="pl"][contains(text(),"出品方:")]/following::text()[1] | //div[@id="info"]//span[@class="pl"][contains(text(),"出品方:")]/following::text()[2]')
        publish_author = self.judge_num(publish_author)
        translator = tree.xpath(
            '//div[@id="info"]//span[@class="pl"][contains(text(),"译者")]/following::text()[1] | //div[@id="info"]//span[@class="pl"][contains(text(),"译者")]/following::text()[2]')
        translator = self.judge_num(translator)
        publish_year = tree.xpath(
            '//div[@id="info"]//span[@class="pl"][contains(text(),"出版年:")]/following::text()[1] | //div[@id="info"]//span[@class="pl"][contains(text(),"出版年:")]/following::text()[2]')
        publish_year = self.judge_num(publish_year)
        page = tree.xpath(
            '//div[@id="info"]//span[@class="pl"][contains(text(),"页数:")]/following::text()[1] | //div[@id="info"]//span[@class="pl"][contains(text(),"页数:")]/following::text()[2]')
        page = self.judge_num(page)
        decoration = tree.xpath(
            '//div[@id="info"]//span[@class="pl"][contains(text(),"装帧:")]/following::text()[1] | //div[@id="info"]//span[@class="pl"][contains(text(),"装帧:")]/following::text()[2]')
        decoration = self.judge_num(decoration)
        collection = tree.xpath(
            '//div[@id="info"]//span[@class="pl"][contains(text(),"丛书:")]/following::text()[1] | //div[@id="info"]//span[@class="pl"][contains(text(),"丛书:")]/following::text()[2]')
        collection = self.judge_num(collection)
        ISBN = tree.xpath(
            '//div[@id="info"]//span[@class="pl"][contains(text(),"ISBN:")]/following::text()[1] | //div[@id="info"]//span[@class="pl"][contains(text(),"ISBN:")]/following::text()[2]')
        isbn = self.judge_num(ISBN)
        author = tree.xpath(
            '//div[@id="info"]//span[@class="pl"][contains(text(),"作者")]/following::text()[1] | //div[@id="info"]//span[@class="pl"][contains(text(),"作者")]/following::text()[2]')
        author = self.judge_num(author)
        price = tree.xpath(
            '//div[@id="info"]//span[@class="pl"][contains(text(),"定价:")]/following::text()[1] | //div[@id="info"]//span[@class="pl"][contains(text(),"定价:")]/following::text()[2]')
        price = self.judge_num(price)
        average_rate = tree.xpath('//strong[@class="ll rating_num "]/text()')[0].strip()
        book_name = tree.xpath('//span[@property="v:itemreviewed"]/text()')[0]
        data["book_name"] = book_name
        data["author"] = author
        data["ISBN"] = isbn
        data["collection"] = collection
        data["decoration"] = decoration
        data["average_rate"] = average_rate
        data["page"] = page
        data["translator"] = translator
        data["publish_year"] = publish_year
        data["publish_author"] = publish_author
        data["publish"] = publish
        data["price"] = price
        self.write_to_csv(data)


    def close_spider(self):
        self.fp.close()


    def main(self):
        urls = self.parse_page()
        self.parse(urls)
        self.close_spider()


    def judge_num(self,obj_1):
        data = []
        if obj_1 is not None:
            for item in obj_1:
                item = str(item).strip().replace(":", "")
                if item is not None and "\xa0" not in item and len(item) != 0:
                    data.append(item)
            return ''.join(data)
        else:
            return "无"



if __name__ == '__main__':
    douban().main()