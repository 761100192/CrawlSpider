import time
import requests
import json
import base64
from lxml import etree
import random

requests.packages.urllib3.disable_warnings()


def get_suuid(answer,uuid):
    url = "https://weixin.sogou.com/antispider/thank.php"
    headers = {
        'Host': 'weixin.sogou.com',
        'Connection': 'keep-alive',
        'Content-Length': '196',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://weixin.sogou.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://weixin.sogou.com/antispider/?from=%2fweixin%3Fquery%3dAI%26_sug_type_%3d%26s_from%3dinput%26_sug_%3dn%26type%3d2%26page%3d7%26ie%3dutf8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'ssuid=1729882676; sw_uuid=9391431698; IPLOC=CN4404; SUID=A0F792775118910A000000005FEEAD79; SUV=00F97DBC71404B135FF45C509C209829; SMYUV=1610971822003504; UM_distinctid=177156737b8178-0c35cc664dc5a2-31346d-fa000-177156737b9c4a; ld=4lllllllll2k5WEZlllllpldEslllllltUxahyllll9llllllklll5@@@@@@@@@@; SNUID=D8979FAEDFE55C2575900D80E07F0774; ABTEST=0|1614932043|v1; weixinIndexVisited=1; JSESSIONID=aaas1ffgXlkrl-9LTvUDx; PHPSESSID=n4ulqttf3ulm60iu7vj025b022'
    }
    data = {
        'c': '{}'.format(answer),
        'r': '%2Fweixin%3Fquery%3DAI%26_sug_type_%3D%26s_from%3Dinput%26_sug_%3Dn%26type%3D2%26page%3D7%26ie%3Dutf8',
        'v': '5',
        'suuid': '',
        'auuid': '{}'.format(uuid)
    }
    doc = requests.post(url, headers=headers, data=data, verify=False).json()
    print(doc['id'])
    return doc["id"]



def get_uuid():
    url = 'https://weixin.sogou.com/antispider/'
    params = {
        'from': '/weixin?query=AI&_sug_type_=&s_from=input&_sug_=n&type=2&page=3&ie=utf8'
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'ssuid=1729882676; sw_uuid=9391431698; IPLOC=CN4404; SUID=A0F792775118910A000000005FEEAD79; SUV=00F97DBC71404B135FF45C509C209829; SMYUV=1610971822003504; UM_distinctid=177156737b8178-0c35cc664dc5a2-31346d-fa000-177156737b9c4a; ld=4lllllllll2k5WEZlllllpldEslllllltUxahyllll9llllllklll5@@@@@@@@@@; SNUID=D8979FAEDFE55C2575900D80E07F0774; ABTEST=0|1614932043|v1; weixinIndexVisited=1; JSESSIONID=aaas1ffgXlkrl-9LTvUDx; PHPSESSID=n4ulqttf3ulm60iu7vj025b022',
        'Host': 'weixin.sogou.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    }
    doc = requests.get(url, headers=headers, params=params, verify=False)
    return doc.headers['UUID'].split(',')[0]

def get_image():
    start_url = 'https://weixin.sogou.com/antispider/util/seccode.php'
    start_headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'ssuid=1729882676; sw_uuid=9391431698; IPLOC=CN4404; SUID=A0F792775118910A000000005FEEAD79; SUV=00F97DBC71404B135FF45C509C209829; SMYUV=1610971822003504; UM_distinctid=177156737b8178-0c35cc664dc5a2-31346d-fa000-177156737b9c4a; ld=4lllllllll2k5WEZlllllpldEslllllltUxahyllll9llllllklll5@@@@@@@@@@; SNUID=D8979FAEDFE55C2575900D80E07F0774; ABTEST=0|1614932043|v1; weixinIndexVisited=1; JSESSIONID=aaas1ffgXlkrl-9LTvUDx; PHPSESSID=n4ulqttf3ulm60iu7vj025b022',
        'Host': 'weixin.sogou.com',
        'Referer': 'https://weixin.sogou.com/antispider/?from=%2fweixin%3Fquery%3dAI%26_sug_type_%3d%26s_from%3dinput%26_sug_%3dn%26type%3d2%26page%3d7%26ie%3dutf8',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    }
    params = {
        'tc': '{}'.format(int(round(time.time(), 3) * 1000))
    }
    doc = requests.get(start_url, headers=start_headers, verify=False, params=params)
    fp = open("code.jpg", "wb")
    fp.write(doc.content)
    fp.close()
    f = open('code.jpg', 'rb')
    img = f.read()
    f.close()
    ret = requests.post('http://127.0.0.1:8820', data={"img": base64.b64encode(img)})
    print(ret.text)
    return ret.text[5:11]


def all_list():
    uuid = get_uuid()
    answer = get_image()
    return get_suuid(answer, uuid)

def get_k_h(url):
    b = int(random.random() * 100) + 1
    a = url.find("url=")
    url = url + "&k=" + str(b) + "&h=" + url[a + 4 + 21 + b: a + 4 + 21 + b + 1]
    return url

def start_request(ssuid):
    headers = {
        "cookie":"SNUID="+ssuid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 FS"
    }
    response = requests.get("https://weixin.sogou.com/weixin?query=AI&_sug_type_=&s_from=input&_sug_=n&type=2&page=7&ie=utf8",headers=headers)
    tree = etree.HTML(response.text)
    li_list = tree.xpath('//ul[@class="news-list"]/li')
    urls = []
    for li in li_list:
        title = li.xpath('./div[@class="txt-box"]//a')[0].xpath('string(.)').strip()
        url = li.xpath('./div[@class="txt-box"]//a/@href')[0].strip()
        url = get_k_h(url)
        author = li.xpath('./div[@class="txt-box"]/div[@class="s-p"]/a/text()')[0].strip()
        content = li.xpath('./div[@class="txt-box"]/p[@class="txt-info"]')[0].xpath('string(.)').strip()
        print({"title":title,"author":author,"content":content,"url":url})
        urls.append("https://weixin.sogou.com/" + url)
    return urls


def parse_detail(urls,ssuid):
    headers = {
        "cookie": "SNUID=" + ssuid,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 FS"
    }
    response = requests.get(urls[0],headers=headers).text
    tree = etree.HTML(response)
    tree.xpath('')


if __name__ == '__main__':
    suuid = all_list()
    urls = start_request(ssuid=suuid)
    parse_detail(urls,ssuid=suuid)