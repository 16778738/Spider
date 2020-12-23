# # _*_coding:UTF-8 _*_
# # 采集代理
# import re
# from urllib import request
# from lxml import etree
#
# test_url = "http://www.httpbin.org/ip"
# local_ip = request.urlopen(test_url).read().decode()
#
# url = "https://ip.jiangxianli.com/blog.html"
# res = request.urlopen(url).read().decode('utf-8')
# # with open('ip.html','w',encoding='utf-8') as w:
# #     w.write(res)
# ele = etree.HTML(res)
# char_url_list = ele.xpath('//h3/a/@href')
# for char_url in char_url_list:
#     res1 = request.urlopen(char_url).read().decode('utf-8')
#     rule = '<p>(.*?)</p>'
#     ip_port_list = re.findall(rule, res)
#     for i in ip_port_list[1:]:
#         ip_port = i.split('@HTTP')[0]
#         ip_port1 = ip_port.lstrip()
#         # print(ip_port1)
#         # 拼接对应的代理格式
#         dict1 = {}
#         dict1['http'] = ip_port1
#         print("开始测试代理{}".format(dict1))
#         # 构建代理handler
#         proxy_handler = request.ProxyHandler(dict1)
#         opener = request.build_opener(proxy_handler)
#         try:
#             now_ip = opener.open(test_url, timeout=4).read().decode()
#             if now_ip != local_ip:
#                 print("代理可以用:{}".format(dict1))
#                 with open("ip.txt", "a") as w:
#                     w.write(str(dict1) + "\n")
#                     print("写入ip{}".format(dict1))
#         except:
#             pass

# # 测试代理
# from urllib import request
#
# test_url = "http://www.httpbin.org/ip"
# local_ip = request.urlopen(test_url).read().decode()
# with open('ip.txt', 'r') as r:
#     ips = r.readlines()
# for ip in ips:
#     proxy_handler = request.ProxyHandler(eval(ip))
#     opener = request.build_opener(proxy_handler)
#     try:
#         now_ip = opener.open(test_url, timeout=4).read().decode()
#         if now_ip != local_ip:
#             print("代理可以用{}".format(ip))
#             with open('ip1.txt', 'a') as w:
#                 w.write(str(ip))
#     except:
#         pass
