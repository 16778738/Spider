# _*_coding:UTF-8 _*_
from urllib import request
from lxml import etree

test_url = "http://www.httpbin.org/ip"
# 获取本机IP
local_ip = request.urlopen(test_url).read().decode()
for page in range(1, 5):
    url = "http://www.nimadaili.com/gaoni/%s/" % page
    res = request.urlopen(url).read().decode('utf-8')
    ele = etree.HTML(res)
    # 匹配IP
    ips = ele.xpath('//tbody/tr/td[1]/text()')
    # 拼接成对应的代理格式
    # {'type':'ip:port'}
    for ip in ips:
        dict1 = {}
        dict1['http'] = ip
        print("开始测试{}".format(dict1))
        # 构建代理handler
        proxy_handler = request.ProxyHandler(dict1)
        opener = request.build_opener(proxy_handler)
        try:
            now_ip = opener.open(test_url, timeout=4).read().decode()
            print(now_ip)
            if now_ip != local_ip:
                print("代理可以用:{}".format(dict1))
                with open("ip.txt", "a") as w:
                    w.write(str(dict1) + "\n")
                    print("写入ip{}".format(dict1))
        except:
            pass

# 测试代理
# from urllib import request
#
# test_url = "http://www.httpbin.org/ip"
# local_ip = request.urlopen(test_url).read().decode()
# with open("ip.txt","r") as r:
#     ips = r.readlines()
# for ip in ips:
#     proxy_handler = request.ProxyHandler(eval(ip))
#     opener = request.build_opener(proxy_handler)
#     try:
#         now_ip = opener.open(test_url,timeout=4).read().decode()
#         print(now_ip)
#         if now_ip != local_ip: #
#             print("代理可用:{}".format(ip))
#             with open("ip.txt","a") as w:
#                 w.write(str(ip)+"\n")
#     except:
#         pass
