import requests
import hashlib
import execjs
import time
import random
class youdao():
    def __init__(self):
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            ,"Referer": "http://fanyi.youdao.com/"
            ,'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=1265583004.797717; OUTFOX_SEARCH_USER_ID="-1667917948@10.169.0.83"; JSESSIONID=aaaJl7eOIHUM35M8IowDx; ___rl__test__cookies=1612059403539'
            ,"X-Requested-With": "XMLHttpRequest"
            ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36 FS"
        }

    def md5(self,word):
        # with open('./md5.js','r',encoding="utf-8") as fp:
        #     dic = execjs.compile(fp.read()).call("func")
        #     print(type(dic))

        ts = str(int(time.time() * 1000))
        salt = ts + str(random.randint(0,9))
        m = hashlib.md5()
        str_ = "fanyideskweb" + word + salt + "Tbh5E8=q6U3EXe+&L[4c@"
        m.update(str_.encode())
        sign = m.hexdigest()
        bv = "3d91b10fc349bc3307882f133fbc312a"
        #i :salt
        return { "ts" : ts,"salt":salt,"sign": sign}

    def main(self):
        word = "option"
        dic = self.md5(word)
        print(dic)
        params = {
            "i": word
            ,"from": "AUTO"
            ,"to": "AUTO"
            ,"smartresult": "dict"
            ,"client": "fanyideskweb"
            ,"salt": dic["salt"]
            ,"sign": dic["sign"]
            ,"lts": dic["ts"]
            ,"bv": "3d91b10fc349bc3307882f133fbc312a"
            ,"doctype":"json"
            ,"version":"2.1"
            ,"keyfrom":"fanyi.web"
            ,"action":"FY_BY_REALTlME"
        }
        print(params)
        print(requests.post(url="http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule",
                            data=params,headers=self.headers).text)

if __name__ == '__main__':
    youdao().main()