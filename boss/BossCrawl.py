from bs4 import BeautifulSoup
import requests
import execjs


class Boss():
    def __init__(self):
        self.headers = {
            # 'cookie':'_bl_uid=Uyk94ja8oXw3tzcmsn9dm9ymjUa0; lastCity=101280100; __zp_seo_uuid__=025d8cfd-8c13-488d-a034-bd04ca6baa01; __g=-; __l=r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Di_ZALYiIQ8WmWAZER9Rp_fd4CIfTv6v_abUDCVOSUpgDSQo25smNl3v3SHTlgyuj%26ck%3D6733.2.68.292.176.174.211.284%26shh%3Dwww.baidu.com%26sht%3D78040160_5_pg%26wd%3D%26eqid%3Dda57778600043e270000000660124e03&l=%2Fwww.zhipin.com%2Fguangzhou%2F&s=1&g=&s=3&friend_source=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1610188118,1610243984,1611724434,1611812359; __fid=b7dfbf5381174b8d872ac61fb291379a; __c=1611812359; __a=74953316.1609683433.1611724441.1611812359.153.10.30.153; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1611830473;'
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36 FS'
        }
        self.url = "https://www.zhipin.com/c101280100/"

    def main(self):
        with open('./encrypt.js','r',encoding='utf-8') as fp:
            js = fp.read()
        token = execjs.compile(js).call('result')
        self.headers['cookie'] = 'Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1611832000; lastCity=100010000; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1611832002; __c=1611832002; __g=-; __a=26366506.1611832002..1611832002.1.1.1.1; ' \
                                 ' __zp_stoken__=' + token
        print(self.headers['cookie'])
        params = {
            'query': 'web前端'
            ,'industry':''
            ,'position':''
            ,'ka': 'hot-position-3'
            'srcReferer: https://www.zhipin.com/guangzhou/'
        }
        response = requests.get(self.url,params=params,headers=self.headers)
        print(response.status_code == 302)
        print(response.text)


if __name__ == '__main__':
    Boss().main()