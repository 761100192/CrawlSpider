import requests
import base64
import re
# 1. 先二进制读图片
with open('code.jpg', 'rb') as f:
    img = f.read()

# 2. 图片 base64 编码一下
# 3. 组装 data 发送 post 请求！端口号是软件上绑定的端口号，默认 8820
ret= requests.post('http://127.0.0.1:8820', data={"img": base64.b64encode(img)})

# 4. 收到返回结果
print(ret.text[5:11])