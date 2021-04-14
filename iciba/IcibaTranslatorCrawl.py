import hashlib
import time
import random
import execjs
import requests
import pymysql


class iciba():
    def __init__(self):
        # pymysql.connect:
        #   第一个参数:地址，
        #   第二个参数：账号
        #   第三个参数：密码
        #   第四个参数:  数据库库名
        # 打开数据库连接
        self.db = pymysql.connect('localhost','root','root','qiubai')
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()
        self.headers = {
            'Referer': 'http://www.iciba.com/'
            ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        self.words = ""

    def calcucate_md5(self):
        md = hashlib.md5()
        e = str(random.random())
        with open("./md5.js", 'r', encoding="utf-8") as f:
            params = str(execjs.compile(f.read()).call("md5")).split("-")
        data = params[1].encode(encoding="utf-8")
        md.update(data)
        params[1] = md.hexdigest()
        print("md5 -->  " + params[1])
        return params


    def insert_data(self,name,paraphrase):
        try:
            name = "'" + name + "'"
            paraphrase = "'" + paraphrase + "'"
            sql = f"INSERT INTO word(name,paraphrase) values({name},{paraphrase})" .format(name,paraphrase)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as ex:
            self.db.rollback()


    def parse_data(self,response):
        dataList = response["message"]
        for word in dataList:
            paraphrase = ""
            name = word["key"]
            print(name)
            count = 0
            for mean in word["means"]:
                paraphrase += mean["part"]
                paraphrase += ','.join(mean["means"])
                count += 1
                if count != len(word["means"]):
                    paraphrase += " - "

            print(paraphrase)
            self.insert_data(name,paraphrase)

    def close_db(self):
        self.db.close()

    def read_from_file(self):
        with open('./3555.txt','r',encoding="utf-8") as f:
            self.words = f.read()
        self.words = str(self.words).split(",")



    def main(self):
        self.read_from_file()
        # print(len(self.words))
        # words = ['word', 'beautiful', 'glasses', 'music', 'lighthouse']
        for item in self.words:
            print("当前的单词为:" + item)
            par = self.calcucate_md5()
            params = {
                'word': item
                , 'nums': '5'
                , 'ck': '709a0db45332167b0e2ce1868b84773e'
                , 'timestamp': par[0]
                , 'client': '6'
                , 'uid': '123123'
                , 'key': '1000006'
                , 'is_need_mean': '1'
                , 'signature': par[1]
            }
            response = requests.get(url="https://dict.iciba.com/dictionary/word/suggestion", params=params,
                                    headers=self.headers).json()
            # print(response)
            self.parse_data(response)
            time.sleep(1.5)
        self.close_db()












if __name__ == '__main__':
    print("程序开始")
    ici = iciba()
    ici.main()



