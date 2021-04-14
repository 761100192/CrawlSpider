import re
import requests
import pymysql
from bs4 import BeautifulSoup
import time
import csv
class job():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 FS',
        }
        # self.fp = csv.writer(open('51job.csv','w',encoding="gbk",newline=''))
        self.db = pymysql.connect('localhost','root','root','qiubai')
        self.cursor = self.db.cursor()




    def close_spider(self):
        self.db.close()

    def parse_detail(self,urls):
        sessions = requests.session()
        dataList = []
        for i in range(0, len(urls)):
            print(f"现在进入:{urls[i]}")
            data = []
            page = sessions.get(url=urls[i], headers=self.headers)
            page.encoding = "gbk"
            html = BeautifulSoup(page.text, "html.parser")
            cn = html.find_all("div", class_="cn")[0]
            job_name = cn.find("h1")["title"]
            company_name = cn.find("a", class_="catn")["title"]
            salary = cn.find("strong").text
            msg = cn.find("p", class_="msg ltype").text
            msg_rep = msg.replace("\xa0", "").split("|")
            # bmsg = html.find_all("div", class_="bmsg job_msg inbox")[0]
            # bmsg_p = str(bmsg.find_all("p"))
            detail = html.find('div',class_="bmsg job_msg inbox").text.strip(" ").strip("\n").strip("/").strip("\\").\
                replace("/","").replace("\\","").replace('"',"").replace("'","")
            if  salary.find('年') == -1 and salary.find('天') == -1  and salary.find('小时') == -1 and len(salary) != 0:
                salary_split = salary.split("-")
                min_salary = float(salary_split[0]) * 10000
                max_salary = re.match('(-?\d+)(\.\d+)',salary_split[1])
                if max_salary is None:
                    max_salary = float(re.match('\d+', salary_split[1]).group()) * 10000
                else:
                    max_salary = float(re.match('(-?\d+)(\.\d+)', salary_split[1]).group()) * 10000
                if len(msg_rep) == 5:
                    request_culture = msg_rep[2]
                    city = msg_rep[0]
                    experience = msg_rep[1]
                    recruit_num = msg_rep[3]
                    publish_date = msg_rep[4]
                elif len(msg_rep) == 4:
                    request_culture = msg_rep[1]
                    city = msg_rep[0]
                    experience = ""
                    recruit_num = msg_rep[2]
                    publish_date = msg_rep[3]
                else:
                    request_culture = ""
                    city = msg_rep[0]
                    experience = ""
                    recruit_num = msg_rep[1]
                    publish_date = msg_rep[2]
                # job_name company_name request_culture city min_salary max_salary experience recruit_num publish_date detail
                data.append(job_name)
                data.append(company_name)
                data.append(request_culture)
                data.append(city)
                data.append(min_salary)
                data.append(max_salary)
                data.append(experience)
                data.append(recruit_num)
                data.append(publish_date)
                data.append(detail)
                dataList.append(data)
        return dataList

    def start_request(self):
        pages = []
        for page in range(1,21):
            url = f"https://search.51job.com/list/01,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,{page}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
            response = requests.get(url=url,headers=self.headers).text
            parser = BeautifulSoup(response,'html.parser')
            ret = str(parser.find_all("script")[8])
            ret = ret.replace("\\/", "/")
            urls = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", ret,re.I)
            for item in urls:
                it = str(item)
                if "b&t=0" in it:
                    pages.append(it)
        return pages



    def write_to_csv(self,dataList):
        col_names = ["job_name","company_name","request_culture","city","min_salary","max_salary","work_experience","recruit_num","publish_date","detail"]
        self.fp.writerow(col_names)
        self.fp.writerows(dataList)


    def write_to_mysql(self,dataList):
        try:
            for item in dataList:
                # print(f'insert into 51job values("{item[0]}","{item[1]}","{item[2]}","{item[3]}","{item[4]}",{item[5]},"{item[6]}","{item[7]}","{item[8]}","{item[9]}")'
                #                 .format(str(item[0]),str(item[1]),str(item[2]),str(item[3]),str(item[4]),str(item[5]),str(item[6]),str(item[7]),str(item[8]),str(item[9])))
                self.cursor.execute(f'insert into 51job values("{item[0]}","{item[1]}","{item[2]}","{item[3]}",{item[4]},{item[5]},"{item[6]}","{item[7]}","{item[8]}","{item[9]}")'
                                .format(str(item[0]),str(item[1]),str(item[2]),str(item[3]),str(item[4]),str(item[5]),str(item[6]),str(item[7]),str(item[8]),str(item[9])))
                self.db.commit()
        except Exception as ex:
            print(ex)
            self.db.rollback()



    def main(self):
        urls = self.start_request()
        dataList = self.parse_detail(urls)
        # print('开始csv输出:')
        # self.write_to_csv(dataList)
        print("开始mysql持久化存储")
        self.write_to_mysql(dataList)
        self.close_spider()






if __name__ == '__main__':
    print("start....")
    job().main()