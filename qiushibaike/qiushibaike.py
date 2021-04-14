import requests
import re
import csv


class qiushibaike:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 FS"
        }
        self.fp = open("./qiushibaike.csv","w",encoding="utf-8")
        self.csver = csv.writer(self.fp)

    def parse(self,response):
        data = re.findall(r'<div class="content">\s*<span>\s*(.+)', response)
        self.write_to_csv(data)


    def write_to_csv(self,data):
        self.csver.writerow(["content"])
        self.csver.writerows(data)

    def main(self):
        response = requests.get("https://www.qiushibaike.com/text/",headers=self.headers).text
        self.parse(response)
        self.close()

    def close(self):
        self.fp.close()



if __name__ == '__main__':
    qiushibaike().main()