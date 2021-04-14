import pandas as pd
import time


class data_procession:
    def __init__(self):
        filename = "./" + time.strftime("%Y-%m-%d") + "/" + time.strftime("%Y-%m-%d") + ".csv"
        self.df = pd.read_csv(filename,encoding="utf-8")

    def update_num(self,num):
        if "万" in num:
            return float(num.replace("万", "")) * 10000
        return num

    def main(self):
        self.df["view"] = self.df["view"].apply(self.update_num)
        self.df["danmu_num"] = self.df["danmu_num"].apply(self.update_num)
        filename = "./" + time.strftime("%Y-%m-%d") + "/"+ time.strftime("%Y-%m-%d",time.localtime()) + "_清洗.csv"
        self.df.to_csv(filename,index=False, encoding="utf-8")





if __name__ == '__main__':
    data_procession().main()