import pandas as pd

baidu_csv = pd.read_csv("baidu_1.csv", encoding="utf-8")
baidu_csv["title"].drop_duplicates(keep="first",inplace=True)
baidu_csv.to_csv("baidu_1.csv",index=False)