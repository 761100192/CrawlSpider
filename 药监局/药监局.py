import requests
import json
import csv

class yaojianju:
    def __init__(self):
        self.fp = open("yaojianju.csv","w",encoding="utf-8",newline="")
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
        }
        self.csver = csv.writer(self.fp)
        self.csver.writerow(['businessLicenseNumber', 'businessPerson',
         'certStr', 'cityCode', 'countyCode',
         'creatUser', 'createTime', 'endTime', 'epsAddress',
         'epsName', 'epsProductAddress', 'id',
         'isimport', 'legalPerson', 'offDate', 'offReason', 'parentid', 'preid',
         'processid', 'productSn', 'provinceCode', 'qfDate',
         'qfManagerName', 'qualityPerson', 'rcManagerDepartName',
         'rcManagerUser', 'startTime', 'warehouseAddress', 'xkCompleteDate',
         'xkDate', 'xkDateStr', 'xkName', 'xkProject', 'xkRemark',
         'xkType'])
        self.dataList = []


    def response_hander(self,url,data):
        response =  requests.post(url,data=data)
        return response


    def write_to_csv(self):
        for item in self.dataList:
            data = [item['businessLicenseNumber'], item['businessPerson'],
             item['certStr'], item['cityCode'], item['countyCode'],
             item['creatUser'], item['createTime'], item['endTime'], item['epsAddress'],
             item['epsName'], item['epsProductAddress'], item['id'],
             item['isimport'], item['legalPerson'], item['offDate'], item['offReason'], item['parentid'], item['preid'],
             item['processid'], item['productSn'], item['provinceCode'], item['qfDate'],
             item['qfManagerName'], item['qualityPerson'], item['rcManagerDepartName'],
             item['rcManagerUser'], item['startTime'], item['warehouseAddress'], item['xkCompleteDate'],
             item['xkDate'], item['xkDateStr'], item['xkName'], item['xkProject'], item['xkRemark'],
             item['xkType']]
            self.csver.writerow(data)


    def get_page(self):
        for page in range(1, 6):
            data = {
                "on": "true"
                , "page": page
                , "pageSize": "15"
                , "productName": ""
                , "conditionType": "1"
                , "applyname": ""
                , "applysn": ""
            }
            response = self.response_hander("http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList",data)
            data_list = response.json()["list"]
            for data in data_list:
                id = data["ID"]
                self.parse_detail(id)

    def parse_detail(self,id):
        form_data = {
            "id": id
        }
        response = self.response_hander("http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById",form_data).json()
        print(response)
        self.dataList.append(response)


    def main(self):
        self.get_page()
        self.write_to_csv()

if __name__ == '__main__':
    yaojianju().main()