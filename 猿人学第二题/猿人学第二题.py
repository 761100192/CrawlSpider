#!/usr/bin/env python
# coding: utf-8
import requests
from lxml import etree
from collections import Counter


headers = {
    "Host": "match.yuanrenxue.com"
    ,"Connection": "keep-alive"
    ,"Accept": "application/json, text/javascript, */*; q=0.01"
    ,"User-Agent": "yuanrenxue.project"
    ,"X-Requested-With": "XMLHttpRequest"
    ,"Referer": "http://match.yuanrenxue.com/match/3"
    ,"Accept-Encoding": "gzip, deflate"
    ,"Accept-Language": "zh-CN,zh;q=0.9"
}
session_ = requests.session()
session_.headers = headers



nums = []

for item in range(1,6):
    logo = session_.get(url="http://match.yuanrenxue.com/logo")
    ns = session_.get(url=f"http://match.yuanrenxue.com/api/match/3?page={item}".format(item),headers=headers).json()["data"]
    print(ns)
    for n in ns:
        nums.append(n["value"])


print(nums)

counter = Counter(nums)
dic = dict(counter)
k = 10
print(counter.most_common(k))



