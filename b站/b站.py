import os
import time


dirs = os.listdir()
flag = 0
filepath = time.strftime("%Y-%m-%d")
for file in dirs:
    if file == filepath:
        flag = 1
if flag != 1:
        os.makedirs(filepath + "/danmu", 755);
path = "./"
#
# os.makedirs( path,755);
#
# print()