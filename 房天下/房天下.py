import os
import pymysql
import json
import requests
import time
from lxml import etree
import csv
from bs4 import BeautifulSoup


class fangtianxia:
    def __init__(self):
        self.headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
        }
        self.filepath = "F:\Python\Request模块\yuanrenxue\房天下"
        self.filename = "fangtianxia-" + time.strftime("%Y-%m-%d")
        self.csv_fp = open(os.path.join(self.filepath,self.filename + ".csv"),"w",encoding="utf-8",newline="")
        self.csver = csv.writer(self.csv_fp)
        self.csver.writerow(["name","price","house_type",
                    "area","house_facing_direction",
                    "decoration","is_contain_elevator"])
        self.json_fp = open(os.path.join(self.filepath, self.filename + ".json"), "w", encoding="utf-8")
        self.json_fp.write("[\n")
        # self.db = pymysql.connect("localhost","root","root","job")
        # self.cursor = self.db.cursor()
        self.dataList = []



    def write_to_csv(self,item):
        self.csver.writerow([item["name"],item["price"],item["house_type"],
                    item["area"],item["house_facing_direction"],
                    item["decoration"],item["is_contain_elevator"]])



    def write_to_mysql(self,item):
        sql = "insert into fangtianxia values(%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,(item["name"],item["price"],item["house_type"],
                    item["area"],item["house_facing_direction"],
                    item["decoration"],item["is_contain_elevator"]))
        self.db.commit()



    def write_to_json(self,item):
        data = json.dumps(item,ensure_ascii=False)
        self.json_fp.write(data)
        self.json_fp.write("\n")



    def response_handler(self,url):
        response = requests.get(url,headers=self.headers)
        return response



    def parse_detail(self,urls):
        #img[@class="img-bg"]
        for url in urls:
            response = self.response_handler(url).text
            tree = etree.HTML(response)
            t4 = tree.xpath('//script[1]/text()')[1][
            tree.xpath('//script[1]/text()')[1].find("t4=") + 4:tree.xpath('//script[1]/text()')[1].find(
                "var t4=") + 55]
            t3 = tree.xpath('//script[1]/text()')[1][tree.xpath('//script[1]/text()')[1].find("rfss="):tree.xpath('//script[1]/text()')[1].find("rfss=") + 28]
            response = self.response_handler(t4 + "?" + t3).text
            print("现在访问:{url}".format(url=t4 + "?" + t3))
            tree = etree.HTML(response)
            name = tree.xpath('//span[@class="tit_text"]/text()')
            if len(name) != 0:
                name = name[0].strip()
                price = tree.xpath('//span[@class="zf_mianji"]/b/text()')[0].strip()
                house_type = tree.xpath('//div[@class="tt"]/text()')[0].strip()
                area = tree.xpath('/html/body/div[4]/div[1]/div[4]/div[4]/div[2]/div[1]/text()')[0].strip()
                house_facing_direction = tree.xpath('//div[@class="tr-line clearfix"][2]/div[@class="trl-item1 w146"]/div[1]/text()')[0].strip()
                decoration = tree.xpath('//div[@class="tr-line clearfix"][2]/div[@class="trl-item1 w132"]/div[1]/text()')[0].strip()
                is_contain_elevator = tree.xpath('//div[@class="cont clearfix"]/div[2]/span[1]/text()')[0].strip()
                data = {"name":name,"price":price,"house_type":house_type,
                        "area":area,"house_facing_direction":house_facing_direction,
                        "decoration":decoration,"is_contain_elevator":is_contain_elevator}
                self.dataList.append(data)
            time.sleep(2)




    def parse_url(self,response):
        print(type(response))
        tree = etree.HTML(response)
        tag = tree.xpath('//script[1]/text()')[1]
        a = tag.find("rfss")
        return tag[a:a+28]

    def parse(self):
        urls = []
        for page in range(1,9):
            print("现在进入搜索页:{page}".format(page=page))
            url = "https://zh.esf.fang.com/house/i3{page}".format(page=page)
            response_url = self.response_handler(url).text
            params = self.parse_url(response_url)
            response = self.response_handler(url + "?" + params).text
            tree = etree.HTML(response)
            dl_list = tree.xpath('//div[@class="shop_list shop_list_4"]/dl')
            for dl in dl_list:
                url = dl.xpath('.//h4[@class="clearfix"]/a/@href')
                if len(url) != 0:
                    print(url)
                    url = "https://zh.esf.fang.com" + url[0]
                    urls.append(url)
            time.sleep(2)
        return urls

    def close_spider(self):
        self.json_fp("\n]")
        self.csv_fp.close()
        self.json_fp.close()
        # self.cursor.close()
        # self.db.close()


    def main(self):
        urls = self.parse()
        self.parse_detail(urls)
        # self.write_to_mysql()
        # self.write_to_csv()
        # self.write_to_json()
        self.close_spider()




if __name__ == '__main__':
    fangtianxia().main()
