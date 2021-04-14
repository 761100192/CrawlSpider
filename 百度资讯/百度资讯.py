from lxml import etree
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import csv
import time
from bs4 import BeautifulSoup

class baidu:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.baidu_csv = pd.read_csv("baidu_keywords.csv",encoding="gbk")
        self.keywords = self.baidu_csv["keywords"].values.tolist()[1161:1253]
        self.fp = open("baidu.csv","w",encoding="utf-8",newline="")
        self.csver = csv.writer(self.fp)
        self.csver.writerow(["name","title","timestamp","link"])

    def write_to_csv(self,data):
        self.csver.writerows(data)



    def parse(self,content,keyword):
        dataList = []
        tree = etree.HTML(content)
        div_list = tree.xpath('//div[@id="content_left"]/div/div/div')
        for div in div_list:
            name = keyword
            data = []
            flag = div.xpath('./h3[@class="news-title_1YtI1"]/a/em/text()')
            if len(flag) == 0:
                pass
            elif name not in flag[0]:
                pass
            else:
                title = ''.join(div.xpath('./h3[@class="news-title_1YtI1"]/a/text() | ./h3[@class="news-title_1YtI1"]/a/em/text()'))
                timestamp = div.xpath('.//div[@class="news-source"]/span[@class="c-color-gray2 c-font-normal"]/text()')
                if len(timestamp) == 0:
                    timestamp = "无"
                else:
                    timestamp = timestamp[0]
                link = div.xpath('./h3[@class="news-title_1YtI1"]/a/@href')[0]
                data.append(name)
                data.append(title)
                data.append(timestamp)
                data.append(link)
                dataList.append(data)
        self.write_to_csv(dataList)

    def start_request(self):
        for keyword in self.keywords:
            try:
                count = 0
                url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=intitle%3A{keyword}&medium=0&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&x_bfe_rqs=03E80000001&x_bfe_tjscore=0.100000&pn=0'\
                    .format(keyword=keyword)
                print("正在爬取关键字:"+ keyword + "-" + str(count))
                page = BeautifulSoup(self.driver.page_source)
                vcode = page.find_all("div",class_="vcode-body vcode-body-spin")
                if len(vcode) != 0:
                    time.sleep(10)
                self.driver.get(url)
                time.sleep(2)
                self.parse(self.driver.page_source,keyword)
                count += 1
                self.driver.set_page_load_timeout(100)
                while True:
                    try:
                        print("正在爬取关键字:" + keyword + "-" + str(count))
                        if count > 1:
                            self.driver.find_element_by_xpath("//div[@id='page']/div[@class='page-inner']/a[@class='n'][2]")
                            self.driver.find_element_by_xpath("//div[@id='page']/div[@class='page-inner']/a[@class='n'][2]").click()
                            self.driver.set_page_load_timeout(5)
                        else:
                            self.driver.find_element_by_xpath("//div[@id='page']/div[@class='page-inner']/a[@class='n']")
                            self.driver.find_element_by_xpath("//div[@id='page']/div[@class='page-inner']/a[@class='n']").click()
                            self.driver.set_page_load_timeout(5)
                        self.parse(self.driver.page_source,keyword)
                        count += 1
                    except NoSuchElementException:
                        break
            except TimeoutException:
                pass


    def close_spider(self):
        self.fp.close()
        self.driver.close()


    def main(self):
        self.start_request()
        self.close_spider()


if __name__ == '__main__':
    baidu().main()