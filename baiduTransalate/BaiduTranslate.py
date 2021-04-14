# coding:utf-8
import requests
import execjs
import json
import re

class baidu_translate():

    def __init__(self):
        self.headers = {
            "Cookie": "BIDUPSID=C43DDD558A35F1FCDCD713A929A93800; PSTM=1614228238; __yjs_duid=1_1293ce1ba50607b8c75d416d915ad0db1614234724917; BAIDUID=04D7BF8DAAD9C052A055471404A0A597:FG=1; BDUSS=ttcHJTUjUwZG9SVXJrQmRQbzkyc1lwMGtTT1oyRERnNnJvOXNlYmFIT0NyMjlnSVFBQUFBJCQAAAAAAAAAAAEAAADJqBmH1MK2wL~Vyb1KYXNvbgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIIiSGCCIkhgck; BDUSS_BFESS=ttcHJTUjUwZG9SVXJrQmRQbzkyc1lwMGtTT1oyRERnNnJvOXNlYmFIT0NyMjlnSVFBQUFBJCQAAAAAAAAAAAEAAADJqBmH1MK2wL~Vyb1KYXNvbgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIIiSGCCIkhgck; H_PS_PSSID=33514_33259_33272_33689_33595_33570_33265; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; delPer=0; PSINO=6; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1615539441; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1615539441; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; __yjsv5_shitong=1.0_7_0de86c7d963dd327ebf72b5e43e2d96fdfc2_300_1615539442916_113.64.72.91_53297e59; ab_sr=1.0.0_ZmI2ZTUwODMxMjA4Yjg4ZDJhNTA2NTYwN2QxMDhjOTkxYTY0MWQ3NmI5ZTI1NDExNzhlNzc4MjExYjNhNTJlOWRkYzNmN2I5ZWI4NjI1NGQ2MGE0OGRlZjU3ZjQ5NmY4"
            ,'Referer': 'https://fanyi.baidu.com/?aldtype=16047'
            ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 FS'
        }


    def main(self):

        query_words = ["option","password","result","header","python"]


        for word in query_words:
            with open('./BaiduTranslateCrawl.js','r',encoding="utf-8") as f:
                sign = execjs.compile(f.read()).call('e',word)
            params = {
              'from': 'en'
              ,'to': 'zh'
              ,'query':word
                ,'simple_means_flag': '3'
                ,'sign': sign
                ,'token': '04e8f8513a0e166681aa5d622a019a2a'
                ,'domain': 'common'
            }
            response = requests.post(url="https://fanyi.baidu.com/v2transapi",params=params,headers=self.headers).text
            # print(response)
            print(json.loads(response)["trans_result"]["data"][0]["dst"])



if __name__ == '__main__':
    b = baidu_translate()
    b.main()