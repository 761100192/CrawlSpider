import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import csv
import execjs


class danmu:
    def __init__(self):
        df = pd.read_csv("./" + time.strftime("%Y-%m-%d") + "/" + time.strftime("%Y-%m-%d") + ".csv", encoding="utf-8")
        self.url = "https://api.bilibili.com/x/v1/dm/list.so?oid="
        self.cids = df["cid"].values.tolist()[0:5]
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
        }


    def write_to_csv(self,filename,data,times):
        data = {"弹幕发送时间":data,"原时长":times}
        df = pd.DataFrame(data)
        df.to_csv("./" + time.strftime("%Y-%m-%d") + "/danmu/" + filename,index=False)
        # with open("danmu/" + filename,"w",encoding="utf-8",newline="") as f:
        #     csver = csv.writer(f,delimiter=',')
        #     print(data)
        #     csver.writerow(["弹幕发送时间"])
        #     for item in data:
        #         csver.writerow(item)

    def parse(self):
        count = 1
        for cid in self.cids:
            print("现在正在爬取:{url}".format(url=self.url + cid))
            data = []
            times = []
            response = requests.get(self.url + cid,headers=self.headers).text
            ret = BeautifulSoup(response, "html.parser")
            d_list = ret.find_all("d")
            for d in d_list:
                data.append(str(self.durationTrans(float(d["p"].split(",")[0]))))
                times.append(d["p"].split(",")[0])
            self.write_to_csv(str(count) + "-" + time.strftime("%Y-%m-%d",time.localtime()) + ".csv",data,times)
            count += 1
            time.sleep(2)


    def durationTrans(self,a):
        b = ""
        h = int(a / 3600)
        m = int(a % 3600 / 60)
        s = int(a % 3600 % 60)
        if (h > 0):
            h = '0' + str(h) if h < 10 else h
            b += h + ":"
        m = '0' + str(m) if m < 10 else m
        s = '0' + str(s) if s < 10 else s
        b += str(m) + ":" + str(s)
        return b



    def main(self):
        self.parse()



if __name__ == '__main__':
    danmu().main()