import csv
import requests
import json
import time

class jingzhun:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
            ,"Content-Type": "application/json"
            ,"Cookie": "acw_tc=2760828e16157112786146628ec81bce1bec3d93c71494a376d5252d05ed2f; sajssdk_2015_cross_new_user=1; _kr_p_se=95a83e8f-b559-4248-8c2e-c5a1f215d73f; krid_user_id=1500884664; krid_user_version=5; kr_plus_id=1500884664; kr_plus_token=rGId9RHtafPKpJpKBN98ozvWK2SPO46562_4____; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221500884664%22%2C%22first_id%22%3A%221782fe5b42b43d-07eb3de7cdf5c8-5771133-1024000-1782fe5b42cabc%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221782fe5b42b43d-07eb3de7cdf5c8-5771133-1024000-1782fe5b42cabc%22%7D"
        }
        self.fp = open("./jingzhun.csv","w",encoding="utf-8",newline="")
        self.csver = csv.writer(self.fp)
        self.csver.writerow(["品牌名称",'英文名称','机构官网','成立时间',
                             '主要投资领域','累计投资企业数','基金管理人数','管理基金数',"管理规模区间",
                             "被投公司简称","社保缴纳人数","市值","交易轮次","来源","交易时间",
                             "交易金额","注册资本","实缴资本","累计融资金额",
                             "高精尖产业","国民经济产业",
                             "战略新兴产业","标签",
                             "一句话简介","品牌url","被投公司url"])
        self.ids = []


    def write_to_csv(self,item):
        data = [item["品牌名称"],item["英文名称"],item["机构官网"],item["成立时间"],item["主要投资领域"],
                item["累计投资企业数"],item["基金管理人数"],item["管理基金数"],item["管理规模区间"],
                item["被投公司简称"],item["社保缴纳人数"],item["市值"],item["交易轮次"],
                            item["来源"],item["交易时间"],
                             item["交易金额"],item["注册资本"],item["实缴资本"],item["累计融资金额"],
                             item["高精尖产业"],item["国民经济产业"],
                             item["战略新兴产业"],item["标签"],
                            item["一句话简介"],item["品牌url"],item["被投公司url"]]
        self.csver.writerow(data)

    def response_handler(self,url,data):
        response = requests.post(url,headers=self.headers,data=json.dumps(data))
        return response

    def parse_page(self):
        url = "https://cloud.jingdata.com/api/metadata/data/getLayoutAndDataList"
        for page in range(5,8):
            data = {"moduleInfoId":"InsightOrg",
                    "recordType":"all",
                    "pageSize":20,
                    "currentPage":page,
                    "filters":[],
                    "orders":[]
                    }
            response = self.response_handler(url,data).json()
            for item in response["result"]["data"]["tableData"]:
                dt_page = {}
                try:
                    ti = item["establish_date"] / 1000
                    t = time.localtime(ti)
                except OSError:
                    print(ti)
                str_date = time.strftime("%Y-%m-%d", t)
                dt_page["成立时间"] = str_date
                try:
                    if item["invest_ent_count"] is not None:
                        dt_page["累计投资企业数"] = item["invest_ent_count"]
                    else:
                        dt_page["累计投资企业数"] = "无"
                except KeyError:
                    dt_page["累计投资企业数"] = "无"
                try:
                    if item["fund_num"] is not None:
                        dt_page["管理基金数"] = item["fund_num"]
                    else:
                        dt_page["管理基金数"] = "无"
                except KeyError:
                    dt_page["管理基金数"] = "无"
                try:
                    if item["fund_manager_num"] is not None:
                        dt_page["基金管理人数"] = item["fund_manager_num"]
                    else:
                        dt_page["基金管理人数"] = "无"
                except KeyError:
                    dt_page["基金管理人数"] = "无"
                brand_name = item["name"]
                brand_id = item["id"]
                if item["en_name"] is not None:
                    dt_page["英文名称"] = item["en_name"]
                else:
                    dt_page["英文名称"] = "无"
                if item["website"] is not None:
                    dt_page["机构官网"] = item["website"]
                else:
                    dt_page["机构官网"] = "无"
                primary_industry_tags = []
                if item["primary_industry"] is not None:
                    for item in item["primary_industry"]:
                        primary_industry_tags.append(item["name"])
                    dt_page["主要投资领域"] = ','.join(primary_industry_tags)
                else:
                    dt_page["主要投资领域"] = "无"
                brand_url = "https://cloud.jingdata.com/#/insight/InsightOrg/" + str(brand_id)
                self.parse(brand_id,brand_name,brand_url,dt_page)



    def parse(self,brand_id,brand_name,brand_url,dt_page):
        url = "https://cloud.jingdata.com/api/metadata/relatedDataByReference"
        data = {
            "apiName": "InsightOrg",
            "dataId": brand_id,
            "relatedListName": "org_invest_case_related_org",
            "targetDescribeApiName": "InsightOrgInvestCase",
            "layoutApiName": "ID_InsightOrgInvestCase_relatedItems_2",
            "pageSize": 20,
            "currentPage": 1,
            "orders": [{"fieldName": "invest_date", "asc": "false"}],
            "pattern": ""
        }
        print("正在爬取{name}第{page}页".format(name=brand_name, page=1))
        try:
            response = self.response_handler(url, data).json()
            total = response["result"]["total"]
        except KeyError:
            response = self.response_handler(url, data).json()
            total = response["result"]["total"]
        pages = total / 20
        for item in response["result"]["data"]["tableData"]:
            dt = {}
            dt["被投公司简称"] = item["com_full_name"][0]["name"]
            value = item["com_full_name"][0]["value"]
            dt["交易轮次"] = item["phase"]
            if item["detail"][0]["name"] is not None:
                dt["来源"] = item["detail"][0]["name"]
            else:
                dt["来源"] = "无"
            tag_names = []
            if item["industry"] is not None:
                for tag in item["industry"]:
                    tag_names.append(tag["name"])
                dt["标签"] = ','.join(tag_names)
            else:
                dt["标签"] = "无"
            if item["finance_amount"] is not None:
                dt["交易金额"] = item["finance_amount"]["currency"] + ":" + item["finance_amount"]["num"]
            else:
                dt["交易金额"] = "无"
            ti = item["invest_date"] / 1000
            t = time.localtime(ti)
            str_date = time.strftime("%Y-%m-%d", t)
            dt["交易时间"] = str_date
            dt["一句话简介"] = item["short_description"]
            dt["品牌名称"] = brand_name
            dt["品牌url"] = brand_url
            dt["英文名称"] = dt_page["英文名称"]
            dt["机构官网"] = dt_page["机构官网"]
            dt["成立时间"] = dt_page["成立时间"]
            dt["主要投资领域"] = dt_page["主要投资领域"]
            dt["累计投资企业数"] = dt_page["累计投资企业数"]
            dt["基金管理人数"] = dt_page["基金管理人数"]
            dt["管理基金数"] = dt_page["管理基金数"]
            dt["管理规模区间"] = ""
            self.parse_detail(value, dt)
        for page in range(2,int(pages) + 1):
            dt = {}
            print("正在爬取{name}第{page}页".format(name=brand_name,page=page))
            data = {
                "apiName": "InsightOrg",
                "dataId": brand_id,
                "relatedListName": "org_invest_case_related_org",
                "targetDescribeApiName": "InsightOrgInvestCase",
                "layoutApiName": "ID_InsightOrgInvestCase_relatedItems_2",
                "pageSize": 20,
                "currentPage": page,
                "orders": [{"fieldName": "invest_date", "asc": "false"}],
                "pattern": ""
            }
            response = self.response_handler(url,data).json()
            try:
                for item in response["result"]["data"]["tableData"]:
                    dt["被投公司简称"] = item["com_full_name"][0]["name"]
                    value = item["com_full_name"][0]["value"]
                    dt["交易轮次"] = item["phase"]
                    if item["detail"] is not None:
                        try:
                            dt["来源"] = item["detail"][0]["name"]
                        except KeyError:
                            dt["来源"] = item["detail"][0]["title"]
                    else:
                        dt["来源"] = "无"
                    tag_names = []
                    if item["industry"] is not None:
                        for tag in item["industry"]:
                            tag_names.append(tag["name"])
                        dt["标签"] = ','.join(tag_names)
                    else:
                        dt["标签"] = "无"
                    if item["finance_amount"] is not None:
                        dt["交易金额"] = item["finance_amount"]["currency"] + ":" + item["finance_amount"]["num"]
                    else:
                        dt["交易金额"] = "无"
                    ti = item["invest_date"] / 1000
                    t = time.localtime(ti)
                    str_date = time.strftime("%Y-%m-%d", t)
                    dt["交易时间"] = str_date
                    dt["一句话简介"] = item["short_description"]
                    dt["品牌名称"] = brand_name
                    dt["品牌url"] = brand_url
                    dt["英文名称"] = dt_page["英文名称"]
                    dt["机构官网"] = dt_page["机构官网"]
                    dt["成立时间"] = dt_page["成立时间"]
                    dt["主要投资领域"] = dt_page["主要投资领域"]
                    dt["累计投资企业数"] = dt_page["累计投资企业数"]
                    dt["基金管理人数"] = dt_page["基金管理人数"]
                    dt["管理基金数"] = dt_page["管理基金数"]
                    dt["管理规模区间"] = ""
                    self.parse_detail(value,dt)
            except KeyError:
                print(KeyError)



    def parse_detail(self,value,dt):
        url = "https://cloud.jingdata.com/api/metadata/relatedDataByReference"
        datail_data = {"apiName": "InsightCompany",
                       "dataId": value,
                       "relatedListName": "company_relation_related_company",
                       "targetDescribeApiName": "InsightCompany",
                       "layoutApiName": "ID_InsightCompany_relatedItems_4",
                       "pageSize": 1,
                       "currentPage": 1,
                       "filters": [],
                       "orders": []}
        print("正在爬取详情页....")
        try:
            response = self.response_handler(url,datail_data).json()
            industrys = []
            if len(response["result"]["data"]["tableData"]) > 0:
                for industry in response["result"]["data"]["tableData"][0]["industry"]:
                    industrys.append(industry["label"])
                dt["国民经济产业"] = ','.join(industrys)
                if response["result"]["data"]["tableData"][0]["reg_capital"] is not None:
                    dt["注册资本"] = response["result"]["data"]["tableData"][0]["reg_capital"]["currency"] + ":" + str(response["result"]["data"]["tableData"][0]["reg_capital"]["value"])
                else:
                    dt["注册资本"] = "无"
                if response["result"]["data"]["tableData"][0]["total_financing_amount"] is not None:
                    dt["累计融资金额"] = response["result"]["data"]["tableData"][0]["total_financing_amount"]["currency"] + ":" + response["result"]["data"]["tableData"][0]["total_financing_amount"]["num"]
                else:
                    dt["累计融资金额"] = "无"
                if response["result"]["data"]["tableData"][0]["paid_capital"] is not None:
                    dt["实缴资本"] = response["result"]["data"]["tableData"][0]["paid_capital"]["currency"] + ":" + response["result"]["data"]["tableData"][0]["paid_capital"]["num"]
                else:
                    dt["实缴资本"] = "无"
                industrial_tags = []
                if response["result"]["data"]["tableData"][0]["industrial_tag"] is not None:
                    for industrial_tag in response["result"]["data"]["tableData"][0]["industrial_tag"]:
                        industrial_tags.append(industrial_tag["name"])
                    dt["战略新兴产业"] = ','.join(industrial_tags)
                else:
                    dt["战略新兴产业"] = "无"
                advance_tags = []
                if response["result"]["data"]["tableData"][0]["advanced1"] is not None:
                    for item in response["result"]["data"]["tableData"][0]["advanced1"]:
                        if len(item) > 0:
                            for it in item:
                                advance_tags.append(it["name"])
                    dt["高精尖产业"] = ','.join(advance_tags)
                else:
                    dt["高精尖产业"] = "无"
                dt["社保缴纳人数"] = response["result"]["data"]["tableData"][0]["employee_num"]
                dt["市值"] = response["result"]["data"]["tableData"][0]["market_value"]
                if type(dt["市值"]) == dict:
                    dt["市值"] = "无"

                if dt["市值"] == None:
                    dt["市值"] = "无"
                dt["被投公司url"] = "https://cloud.jingdata.com/#/insight/InsightCompany/" + value
            else:
                dt["社保缴纳人数"] = "无"
                dt["市值"] = "无"
                dt["高精尖产业"] = "无"
                dt["注册资本"] = "无"
                dt["累计融资金额"] = "无"
                dt["战略新兴产业"] = "无"
                dt["国民经济产业"] = "无"

            self.write_to_csv(dt)
        except KeyError:
            pass
        # time.sleep(1)


    def main(self):
        self.parse_page()
        self.close_spider()


    def close_spider(self):
        self.fp.close()



if __name__ == '__main__':
    jingzhun().main()
