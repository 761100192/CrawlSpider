import requests
from lxml import etree
import re
import time
import json
import pymysql
import csv

class jd():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36 FS'
        }
        self.dataList = []
        self.db = pymysql.connect('localhost','root','root','qiubai')
        self.cursor = self.db.cursor()
        self.fp = csv.writer(open('jd.csv','a',encoding="gbk",newline=''))

    def parse(self,response):
        tree = etree.HTML(response)
        li_list = tree.xpath('//div[@id="J_goodsList"]/ul/li')
        for li in li_list:
            data = []
            datasku = ''.join(li.xpath('@data-sku'))
            src = 'https:' + li.xpath('.//div[@class="p-img"]//img/@data-lazy-img')[0]
            price = li.xpath('.//div[@class="p-price"]//i/text()')[0]
            phone_name = ''.join(li.xpath('.//div[@class="p-name p-name-type-2"]//em/text()'))
            shop_name = li.xpath('.//div[@class="p-shop"]//a/@title')
            shop_name = (shop_name[0] if len(shop_name) > 0 else "")
            data.append(phone_name)
            data.append(shop_name)
            data.append(price)
            commentCount, goodCount, poorCount, goodRate, allCommentStr = self.parse_comment(datasku)
            data.append(commentCount)
            data.append(goodCount)
            data.append(poorCount)
            data.append(goodRate)
            data.append(allCommentStr)
            data.append(src)
            self.dataList.append(data)


    def writeTocsv(self):
        col_names = ['phone_name','shop_name',"price",'comment_count','good_count',"poor_count","good_rate","hot_comment_str","src"]
        self.fp.writerow(col_names)
        self.fp.writerows(self.dataList)


    def write_to_mysql(self):
        try:
            for data in self.dataList:
                sql = "insert into jd values('%s','%s','%s',%s,%s,%s,%s,'%s','%s')" \
                % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])
                self.cursor.execute(sql)
                self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()



    def parse_comment(self,data_sku):
        try:
            url = f"https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=%s&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1" % (
                data_sku)
            print("????????????????????????:"+ url)
            time.sleep(3)
            response = requests.session().get(url=url,headers=self.headers).text
            result = json.loads(re.match(".*?({.*}).*", response, re.S).group(1))
            commentCount = result["productCommentSummary"]["commentCount"]
            if not commentCount:
                goodCount=0
                poorCount=0
                goodRate=0
                hotComment='?????????'
                return commentCount, goodCount, poorCount, goodRate, hotComment
            else:
                goodCount = result['productCommentSummary']['goodCount']
                poorCount = result['productCommentSummary']['poorCount']
                goodRate = result['productCommentSummary']['goodRate']
                hotComment = result['hotCommentTagStatistics']
                if not hotComment:
                    noComment = "?????????"
                    return commentCount, goodCount, poorCount, goodRate, noComment
                else:
                    maxCount = 3  # ?????????????????????????????????
                    hotCommentCount = len(hotComment)  # ???????????????
                    allComment = []
                    if hotCommentCount > maxCount:  # ???????????????????????????????????????????????????????????????
                        loop = maxCount
                    else:
                        loop = hotCommentCount
                    for i in range(0, loop):  # ??????????????????????????????
                        comment_dict = hotComment[i]
                        comment_str = comment_dict["name"]
                        allComment.append(comment_str)

                        # print(allComment)
                        # ???????????????????????????????????????
                    allCommentStr = " ".join(allComment)
                        # print(allCommentStr)
                    return commentCount, goodCount, poorCount, goodRate, allCommentStr
        except:
            self.parse_comment(data_sku)




    def start_request(self):
        for url in range(27,30):
            url = f"https://search.jd.com/Search?keyword=iphone&suggest=1.his.0.0&page={url}&s=56&click=0".format(url)
            print("??????????????????:" + url)

            request_session = requests.session()
            request_session.keep_alive = False
            response = request_session.get(url=url,headers=self.headers).text
            self.parse(response)

    def main(self):
        print("??????..")
        self.start_request()
        print("??????csv??????....")

        self.writeTocsv()
        print("??????mysql?????????....")
        self.write_to_mysql()
        print("??????....")
        self.close_spider()


    def close_spider(self):
        self.db.close()



if __name__ == '__main__':
    print("????????????.....")
    jd().main()