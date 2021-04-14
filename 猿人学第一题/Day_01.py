import execjs
import requests
import time


def get_page(page,parameter,ua):
    url = "http://match.yuanrenxue.com/api/match/1?page={}&m={}".format(page,parameter)
    params = {
        page:page,
        parameter:parameter
    }
    headers = {
        'Host': 'match.yuanrenxue.com'
        ,'Cookie': 'Hm_lvt_0362c7a08a9a04ccf3a8463c590e1e2f=1610177699,1610178183,1611475324,1611479259; Hm_lpvt_0362c7a08a9a04ccf3a8463c590e1e2f=1611479259; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1610178487,1611475327,1611479261,1611479268; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1611475348,1611479272; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1611479272; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1611479288'
        ,'Referer': 'http://match.yuanrenxue.com/match/1'
        ,'User-Agent':ua
        ,'X-Requested-With':'XMLHttpRequest'
    }
    response = requests.get(url=url,headers=headers)
    # print(response.json())
    print(response.text)
    return response.json()

def caculate():
    with open(r'exec.js',encoding="utf-8",mode='r') as f:
        jsData = f.read()

        psd = execjs.compile(jsData).call('getvalue')
        psd = psd.replace('丨','%E4%B8%A8')
        print("this parameter:" + psd)
        return psd


if __name__ == '__main__':
    sum_num = 0
    index_num = 0
    # ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 FS"
    ua = "yuanrenxue.project"
    for page_num in range(1,6):
        print(page_num)
        if page_num == 4 | page_num == 5:
            ua = "yuanrenxue.project"
            res = get_page(page_num, caculate(),ua)
        else:
            res = get_page(page_num, caculate(), ua)
        data = [__['value'] for __ in res['data']]
        print(data)
        sum_num += sum(data)
        index_num += len(data)
        time.sleep(1)
    average = sum_num / index_num
    print(average)
