import requests
from lxml import etree
import csv
import pymysql

class tianyancha:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 FS"
        }
        self.fp = open("tianyancha.csv","w",encoding="utf-8",newline="")
        self.csver = csv.writer(self.fp)
        self.db = pymysql.connect("localhost","root","root","qiubai")
        self.cursor = self.db.cursor()
        self.dataList = []

    def parse(self,response):
        tree = etree.HTML(response)
        div_list = tree.xpath('//div[@class="boss-list"]/div')
        for div in div_list:
            data = []
            name = div.xpath('.//div[@class="content"]/div[@class="title "]/@title')[0].strip().replace("<em>","").replace("</em>","")
            print(name)
            tag = div.xpath('.//div[@class="content"]/span[@class="tag-common -primary-bg ml8"]/text()')[0].strip()
            info = div.xpath('.//div[@class="introduce"]/text()')[0].strip()

            data.append(name)
            data.append(tag)
            data.append(info)
            self.dataList.append(data)


    def close_spider(self):
        self.fp.close()
        self.db.close()


    def write_to_csv(self):
        col_name = ["name","tag","info"]
        self.csver.writerow(col_name)
        self.csver.writerows(self.dataList)

    def write_to_mysql(self):
        for data in self.dataList:
            sql = "insert into tianyancha values('%s','%s','%s')" \
                  % (data[0],data[1],data[2])
            self.cursor.execute(sql)
            self.db.commit()

    def main(self):
        for page in range(1,3):
            response = requests.get("https://www.tianyancha.com/relatedbossorganize?keyOrganize=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4&pn={page}".format(page=page)
                                    ,headers=self.headers).text
            self.parse(response)
        self.write_to_csv()
        self.write_to_mysql()



if __name__ == '__main__':
    tianyancha().main()