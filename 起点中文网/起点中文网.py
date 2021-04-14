import requests
from lxml import etree
import re
import csv
import pymysql

class qidianzhongwenwang:
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 FS"
        }
        self.fp = open("qidianzhongwenwang.csv",'w',encoding="utf-8",newline='')
        self.csver = csv.writer(self.fp)
        self.db = pymysql.connect(host="localhost",user="root",password="root",database="qiubai")
        self.cursor = self.db.cursor()
        self.dataList = []

    def close_spider(self):
        self.fp.close()
        self.db.close()

    def parse(self,response):
        tree = etree.HTML(response)
        li_list = tree.xpath('//div[@class="book-img-text"]/ul/li')
        for li in li_list:
            data = []
            name = li.xpath('.//div[@class="book-mid-info"]/h4/a/text()')[0].strip()
            category = li.xpath('.//p[@class="author"]/a[2]/text()')[0].strip()
            author = li.xpath('.//p[@class="author"]/a[1]/text()')[0].strip()
            type = li.xpath('.//p[@class="author"]/span/text()')[0].strip()
            info = li.xpath('.//p[@class="intro"]/text()')[0].strip()
            update_time = li.xpath('.//p[@class="update"]/span/text()')[0]
            data.append(name)
            data.append(category)
            data.append(author)
            data.append(type)
            data.append(info)
            data.append(update_time)
            self.dataList.append(data)


    def write_to_csv(self):
        col_name = ["name","category","author","type","info","update_time"]
        self.csver.writerow(col_name)
        self.csver.writerows(self.dataList)


    def write_to_mysql(self):
        for data in self.dataList:
            try:
                sql = "insert into qidianzhongwenwang values('%s','%s','%s','%s','%s',str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s'))" \
                      % (data[0], data[1], data[2], data[3], data[4], data[5])
                self.cursor.execute(sql)
                self.db.commit()
            except:
                sql = "insert into qidianzhongwenwang values('%s','%s','%s','%s','%s',str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s'))" \
                      % (data[0], data[1], data[2], data[3], data[4], "2021-" + data[5])
                self.cursor.execute(sql)
                self.db.commit()



    def main(self):
        for page in range(1,6):
            print("正在爬取:https://www.qidian.com/rank/yuepiao?month=01&style=1&page={page}".format(page=page))
            response = requests.get("https://www.qidian.com/rank/yuepiao?month=01&style=1&page={page}".format(page=page),headers=self.headers).text
            self.parse(response)
        self.write_to_csv()
        self.write_to_mysql()


if __name__ == '__main__':
    qidianzhongwenwang().main()