# 导入使用的库
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
from datetime import datetime


# 从职位详情页面内获取职位要求
def getjobneeds(positionId):
    url = 'https://www.lagou.com/jobs/{}.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%AE%BE%E8%AE%A1/p-city_0?px=default',
        'Upgrade-Insecure-Requests': '1'
    }

    s = requests.Session()
    s.get(url.format(positionId), headers=headers, timeout=3)  # 请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    response = s.get(url.format(positionId), headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
    time.sleep(5)  # 休息 休息一下

    soup = BeautifulSoup(response.text, 'html.parser')
    need = ' '.join([p.text.strip() for p in soup.select('.job_bt div')])
    return need


# 获取职位具体信息#获取职位具体
def getjobdetails(jd):
    results = {}
    results['businessZones'] = jd['businessZones']
    results['companyFullName'] = jd['companyFullName']
    results['companyLabelList'] = jd['companyLabelList']
    results['financeStage'] = jd['financeStage']
    results['skillLables'] = jd['skillLables']
    results['companySize'] = jd['companySize']
    results['latitude'] = jd['latitude']
    results['longitude'] = jd['longitude']
    results['city'] = jd['city']
    results['district'] = jd['district']
    results['salary'] = jd['salary']
    results['secondType'] = jd['secondType']
    results['workYear'] = jd['workYear']
    results['education'] = jd['education']
    results['firstType'] = jd['firstType']
    results['thirdType'] = jd['thirdType']
    results['positionName'] = jd['positionName']
    results['positionLables'] = jd['positionLables']
    results['positionAdvantage'] = jd['positionAdvantage']
    positionId = jd['positionId']
    results['need'] = getjobneeds(positionId)
    time.sleep(2)  # 设置暂停时间，控制频率
    print(jd, 'get')
    return results


# 获取整个页面上的职位信息
def parseListLinks(url_start, url_parse):
    jobs = []
    from_data = {'first': 'true',
                 'pn': '1',
                 'kd': '设计'}

    headers = {
        'Host': 'www.lagou.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%AE%BE%E8%AE%A1/p-city_0?px=default',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest',
    }

    res = []
    for n in range(2):
        from_data['pn'] = n + 1
        s = requests.Session()
        s.get(url_start, headers=headers, timeout=3)  # 请求首页获取cookies
        cookie = s.cookies  # 为此次获取的cookies
        response = s.post(url_parse, data=from_data, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
        time.sleep(5)
        res.append(response)
    print(res)

    jd = []
    for m in range(len(res)):
        jd.append(json.loads(res[m].text)['content']['positionResult']['result'])
        print(jd)
    for j in range(len(jd)):
        for i in range(15):
            jobs.append(getjobdetails(jd[j][i]))
            print(jobs)
    time.sleep(30)
    return jobs


def main():
    url_start = "https://www.lagou.com/jobs/list_设计?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput="
    url_parse = "https://www.lagou.com/jobs/positionAjax.json?city=&needAddtionalResult=false"
    jobs_total = parseListLinks(url_start, url_parse)
    now = datetime.now().strftime('%m%d_%H%M%S')
    newsname = 'lagou_sj' + now + '.xlsx'  # 按时间命名文件
    df = pd.DataFrame(jobs_total)
    df.to_excel(newsname)
    print('文件已保存')


if __name__ == '__main__':
    main()