# _*_coding:UTF-8 _*_
import requests

# r = requests.get('https://www.baidu.com')
# print(r)
# print(r.status_code) #状态码
# print(r.text) #解码后的数据
# print(r.content) #二进制流数据
# 乱码的解决方式
# 1.二进制流decode
# print(r.content.decode('utf-8'))
# 2. 设置response.encoding 为指定编码
# r.encoding = 'utf-8'
# print(r.text)

# url = 'https://www.httpbin.org/post'
# data = {
#     "zfy": "nb",
#     "sss": "sss"
# }
# res = requests.post(url,data=data).text
# res = requests.post(url,json=data).text
# print(res)

url = "http://www.httpbin.org/ip"
proxy = {'http':'http://91.205.174.26:80'}
res = requests.get(url,proxies=proxy).text
print(res)

