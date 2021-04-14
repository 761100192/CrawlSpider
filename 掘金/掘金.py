import json
import time
import requests
import csv



class juejin:

    def __init__(self):
        self.headers = {
            "content-type": "application/json"
            ,"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
            ,"cookie": "MONITOR_WEB_ID=a09e6011-044a-4ea4-adb8-f4b9067c79cb; _ga=GA1.2.1410697486.1610197447; passport_csrf_token=d950d3aec25a99afc18f356eee7d9874; passport_csrf_token_default=d950d3aec25a99afc18f356eee7d9874; odin_tt=1863bed2ff1746af81814269dc0e8025e45dc5901fa431077588a55a3c208033a4a4f9575f100b9990484282946d0df131cb99b889fe353bcc49801f556b5cc1; n_mh=9-mIeuD4wZnlYrrOvfzG3MuT6aQmCUtmr8FxV8Kl8xY; sid_guard=48dc9a40bf72f0fbb0a9cd1449e7d160%7C1613403172%7C5184000%7CFri%2C+16-Apr-2021+15%3A32%3A52+GMT; uid_tt=551f639fb3e16e39a50dfed975955277; uid_tt_ss=551f639fb3e16e39a50dfed975955277; sid_tt=48dc9a40bf72f0fbb0a9cd1449e7d160; sessionid=48dc9a40bf72f0fbb0a9cd1449e7d160; sessionid_ss=48dc9a40bf72f0fbb0a9cd1449e7d160; _gid=GA1.2.1549310571.1617503590"
        }
        filename = "juejin-" + time.strftime("%Y-%m-%d",time.localtime()) + ".csv"
        self.fp = open(filename,"w",encoding="utf-8",newline="")
        self.csver = csv.writer(self.fp)
        self.csver.writerow(["author_name","article_title","article_content","tag","category","view_count","comment_count"])


    def write_to_csv(self,item):
        data = [item["author_name"],item["article_title"],item["article_content"],
                item["tag"],item["tag"],item["category"],item["view_count"],item["comment_count"]]
        self.csver.writerow(data)


    def parse(self):
        data = {"id_type":2,
                "client_type":2608,
                "sort_type":200,
                "cursor":"0",
                "limit":20}
        data = json.dumps(data)
        response = requests.post("https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed",
                                 headers=self.headers,data=data).json()
        self.parse_detail(response)


    def parse_detail(self,response):
        for item in response["data"]:
            data = {}
            data["article_content"] = item["item_info"]["article_info"]["brief_content"]
            data["view_count"] = item["item_info"]["article_info"]["view_count"]
            data["comment_count"] = item["item_info"]["article_info"]["comment_count"]
            data["author_name"] = item["item_info"]["author_user_info"]["user_name"]
            data["article_title"] = item["item_info"]["article_info"]["title"]
            tags = item["item_info"]["tags"]
            tag_list = []
            for tag in tags:
                tag_list.append(tag["tag_name"])
            data["tag"] = ','.join(tag_list)
            data["category"] = item["item_info"]["category"]["category_name"]
            self.write_to_csv(data)

    def main(self):
        self.parse()


if __name__ == '__main__':
    juejin().main()