#!/usr/bin/env python
# coding: utf-8



from selenium import webdriver
from lxml import etree
import requests
from bs4 import BeautifulSoup
import time
import csv



class BilibliCrawl:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.rank = []
        self.urls = []
        self.cids = []
        self.filename = "./" + time.strftime("%Y-%m-%d") + "/" + time.strftime("%Y-%m-%d") + ".csv"
        self.fp = open(self.filename,"w",encoding="utf-8",newline="")
        self.csver = csv.writer(self.fp)
        self.csver.writerow(["rank","name","view","comment_num","tag","danmu_num","publish_time","video_time","cid","url"])


    def write_to_csv(self,data):
        self.csver.writerow([self.rank[data["count"]],data["name"],data["view"],data["comment_num"]
                                ,data["tag"],data["danmu_num"],
                             data["publish_time"],data["video_time"],data["cid"],self.urls[data["count"]]])

    def parse(self):
        self.driver.get("https://www.bilibili.com/v/popular/rank/all")
        self.driver.maximize_window()
        tree = etree.HTML(self.driver.page_source)
        self.rank = tree.xpath('//ul/li/div[@class="num"]/text()')
        a_list = self.driver.find_elements_by_xpath('//ul[@class="rank-list"]/li//div[@class="info"]/a')
        self.urls = []
        for a in a_list:
            self.urls.append(a.get_attribute("href"))
        time.sleep(1)

    def parse_detail(self):
        count = 0
        for url in self.urls:
            print("现在正在进入:{page}".format(page=url))
            self.driver.get(url)
            self.driver.implicitly_wait(500)
            # 调用JS代码拖动滚动条
            self.driver.execute_script("window.scrollTo(0,1680)")
            # 直接拖动到底部
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            tree = etree.HTML(self.driver.page_source)
            comment_num = tree.xpath('//span[@class="b-head-t results"]/text()')
            while len(comment_num) == 0:
                time.sleep(3)
                tree = etree.HTML(self.driver.page_source)
                comment_num = tree.xpath('//span[@class="b-head-t results"]/text()')
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            comment_num = comment_num[0]
            name = tree.xpath('//span[@class="tit tr-fix"]/text() | //span[@class="tit"]/text()')[0]
            view = tree.xpath('//span[@class="view"]/text()')[0].replace("·","").replace("播放","").strip()
            danmu_num = tree.xpath('//span[@class="dm"]/text()')[0].replace("弹幕","")
            publish_time = tree.xpath('//div[@class="video-data"]/span[3]/text()')[0]
            video_time = tree.xpath('//span[@class="bilibili-player-video-time-total"]/text()')
            while len(video_time) == 0:
                self.driver.execute_script("window.scrollTo(0,0)")
                time.sleep(2)
                tree = etree.HTML(self.driver.page_source)
                video_time = tree.xpath('//span[@class="bilibili-player-video-time-total"]/text()')
            video_time = video_time[0]
            tags = tree.xpath('//ul[@class="tag-area clearfix"]/li/div/a[@class="tag-link"]/text() | //ul[@class="tag-area clearfix"]/li//a[@class="tag-link"]/span/text()')
            tag_list = []
            for tag in tags:
                tag_list.append(tag.strip())
            tag_list = ','.join(tag_list)
            script = tree.xpath('//script[contains(text(),"cid")]/text()')
            while len(script) == 0:
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                tree = etree.HTML(self.driver.page_source)
                script = tree.xpath('//script[contains(text(),"cid")]/text()')
                time.sleep(2)
            script = script[0]
            cid = script[script.find("upgcxcode/") + 16:script.find("upgcxcode/") + 25]
            self.write_to_csv({"name":name,"view":view,"comment_num":comment_num,
                               "danmu_num":danmu_num,"publish_time":publish_time,
                               "tag":tag_list,"cid":cid,"count":count,"video_time":video_time})
            count += 1
            time.sleep(1)


    def main(self):
        print("开始爬取TOP100......")
        self.parse()
        print("开始爬取详情页..")
        self.parse_detail()
        print("关闭持久化")
        self.close_spider()

    def close_spider(self):
        self.fp.close()
        self.driver.close()

if __name__ == '__main__':
    BilibliCrawl().main()


