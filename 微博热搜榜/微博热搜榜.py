import rsa
import time
import requests
import json
import re
from urllib.parse import parse_qs,urlparse
key = ("10001","","EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443")
e = key[0]
e = int(e, 16)
n = key[-1]
n = int(n, 16)

pub_key = rsa.PublicKey(e=e, n=n)
server_time = time.time()
m = rsa.encrypt('%s\tDM421K\npopo7758'.format(round(server_time)).encode(),pub_key)
sp = m.hex()
data = {
    "entry": "account"
    ,"gateway": "1"
    ,"from": "null"
    ,"savestate": "30"
    ,"useticket": "0"
    ,"pagerefer":""
    ,"wsseretry": "servertime_error"
    ,"vsnf": "1"
    ,"su": "MTU2MjUzNzE0MzA="
    ,"service": "account"
    ,"servertime": "1614844679"
    ,"nonce": "4XCUNK"
    ,"pwencode": "rsa2"
    ,"rsakv": "1330428213"
    ,"sp": sp
    ,"sr": "1280*800"
    ,"encoding": "UTF-8"
    ,"cdult": "3"
    ,"domain": "sina.com.cn"
    ,"prelt": "16"
    ,"returntype": "TEXT"
}
_1 = int(round(server_time * 1000))
data = {
    "uid":""
    ,"ref": "PC_topsug"
    ,"url": "https://s.weibo.com/top/summary"
    ,"Mozilla": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    ,"_cb": "STK_%s" % (_1)
}
# requests.post("")
# timeArray = time.strftime(time.localtime(),"%Y-%m-%d %H:%M:%S")
#转换成时间戳
print(_1)
response = requests.get("https://s.weibo.com/ajax/jsonp/gettopsug",params=data)
print(response.text)
resp = response.text.replace("try{window.","").replace("%s".format(_1),"").replace("STK_","").replace(")}catch(e){}","")
js = re.match(".*?({.*}).*", resp, re.S).group(1)
print(json.loads(js))