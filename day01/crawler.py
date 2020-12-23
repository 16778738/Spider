# _*_coding:UTF-8 _*_
# from urllib import request
# import re
#
# a = 1
# for pn in range(0, 180, 30):
#     url = "https://image.baidu.com/search/acjson?tn=resultjson_com&logid=6804522630827236065&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E9%98%BF%E7%8B%B8&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=%E9%98%BF%E7%8B%B8&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={}&rn=30".format(pn)
#     result = request.urlopen(url).read().decode('utf-8')
#     rule = 'middleURL":"(.*?)"'
#     pic_list = re.findall(rule, result)
#     for i in pic_list:
#         print(i)
#         res = request.urlopen(i).read()
#         with open("./img/"+str(a) + ".jpg", 'wb') as w:
#             w.write(res)
#             a += 1

# # json格式处理
#
# from urllib import request
# import json
#
# a = 1
# for pn in range(0, 180, 30):
#     url = "https://image.baidu.com/search/acjson?tn=resultjson_com&logid=6804522630827236065&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E9%98%BF%E7%8B%B8&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=%E9%98%BF%E7%8B%B8&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={}&rn=30".format(
#         pn)
#     result = request.urlopen(url).read().decode('utf-8')  #生成字符串
#     new_result = json.loads(result)   #生成json对象
#     print(new_result)
#     for data in new_result['data']:
#         img_url = data['middleURL']
#         print(img_url)
#         img_res = request.urlopen(img_url).read()
#         with open("./img/" + str(a) + ".jpg", 'wb') as w:
#             w.write(img_res)
#             a += 1

# 获取笔趣阁小说章节的url
# from lxml import etree
# import gzip
# from urllib import request
#
# url = "http://www.xbiquge.la/xiaoshuodaquan/"
# result = request.urlopen(url).read()
#
# try:
#     res = gzip.decompress(result).decode('utf-8')
# except:
#     res = result.decode('utf-8')
#
# # 构建element对象
# ele = etree.HTML(res)
# print(ele)
# # 基于element的对象进行xpath匹配
# book_urls = ele.xpath('//div[@class="novellist"]//li/a/@href')
# # print(book_urls)
# for book_url in book_urls:
#     booK_res = request.urlopen(book_url).read()
#     try:
#         book_result = booK_res.decode('utf-8')
#     except:
#         book_result = gzip.decompress(booK_res).decode('utf-8')
#     ele = etree.HTML(book_result)
#     chapter_url = ele.xpath('//div[@id="list"]/dl/dd/a/@href')
#     # print(chapter_url, "章节url")  # 获取的章节url为['/15/15409/8163818.html', '/15/15409/8163819.html']
#     book_name = ele.xpath('//h1/text()')[0]
#     # 拼接新的url链接
#     new_chapter_urls = ["http://www.xbiquge.la" + url for url in chapter_url]
#     cha_names = ele.xpath('//div[@id="list"]/dl/dd/a/text()')
#     for cha_url in new_chapter_urls:
#         index = new_chapter_urls.index(cha_url)
#         cha_name = cha_names[index]
#         print(cha_name)
#         with open("./book/" + book_name + ".txt", "a", encoding="utf-8") as w:
#             w.write(cha_name + ":" + cha_url + "\n")

# # 获取笔趣阁小说的内容
# from lxml import etree
# from urllib import request
# import gzip
#
# url = "http://www.xbiquge.la/xiaoshuodaquan/"
# result = request.urlopen(url).read()
# try:
#     res = gzip.decompress(result).decode('utf-8')
# except:
#     res = result.decode('utf-8')
# ele = etree.HTML(res)
# book_urls = ele.xpath('//div[@id="main"]//li/a/@href')
# for book_url in book_urls:
#     book_res = request.urlopen(book_url).read()
#     try:
#         book_result = book_res.decode('utf-8')
#     except:
#         book_result = gzip.decompress(book_res).decode('utf-8')
#     ele = etree.HTML(book_result)
#     chapter_urls = ele.xpath('//div[@id="list"]/dl/dd/a/@href')
#     book_name = ele.xpath('//h1/text()')[0]
#     print(book_name)
#     new_chapter_urls = ["http://www.xbiquge.la" + url for url in chapter_urls]
#     print(new_chapter_urls)
#     for chapter_url in new_chapter_urls:
#         req = request.Request(chapter_url, headers={'user-agent': "baiduSpider"})
#         cha_res = request.urlopen(req).read()
#         try:
#             cha_result = cha_res.decode('utf-8')
#         except:
#             cha_result = gzip.decompress(cha_res).decode('utf-8')
#         ele = etree.HTML(cha_result)
#         content = ele.xpath('//div[@id="content"]/text()')
#         cha_name = ele.xpath('//h1/text()')[0]
#         with open(book_name + ".txt", "a", encoding="utf-8") as w:
#             w.write(cha_name + "\n")
#             for cont in content:
#                 w.write(cont)
#             w.write("\n")





