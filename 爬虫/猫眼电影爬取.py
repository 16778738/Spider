# _*_coding:UTF-8 _*_
import random
import re, gzip
from urllib import request
from lxml import etree

num = 0
with open("ip.txt", "r") as r:
    ips = r.readlines()
for pn in range(0, 100, 10):
    url = "https://maoyan.com/board/4?offset={}".format(pn)
    headers = {
        'user-agent': 'YoudaoBot',
        "referer": url,
    }
    req = request.Request(url, headers=headers)
    for ip in ips:
        # 构建handler
        handler = request.ProxyHandler(eval(ip))
        opener = request.build_opener(handler)
        res = opener.open(req).read().decode('utf-8')
        # 使用xpath匹配信息
        ele = etree.HTML(res)
        # 匹配电影的url
        movie_url_list = ele.xpath('//dl[@class="board-wrapper"]/dd/a/@href')
        # print(movie_url_list)
        # 拼接电影url
        new_movie_url = ["https://maoyan.com" + url for url in movie_url_list]
        # print(new_movie_url)
        for movie_url in new_movie_url:
            # print(movie_url)
            req1 = request.Request(movie_url, headers=headers)
            res1 = request.urlopen(req1).read()
            try:
                result1 = gzip.decompress(res1).decode('utf-8')
            except:
                result1 = res1.decode('utf-8')
            # print(result1)
            ele1 = etree.HTML(result1)
            movie_name = ele1.xpath('//h1/text()')[0]
            rule = '(.*?)\n(.*?)\n(.*?)\n(.*?)<li class="ellipsis">(.*?)<'
            movie_time = re.findall(rule, result1)[0][1][12:]
            movie_countries = re.findall(rule, result1)[0][0][8:]
            movie_grade = ele.xpath('//i[@class="integer"]/text()')[0] + ele.xpath('//i[@class="fraction"]/text()')[0]
            # print(movie_time,movie_countries,movie_grade)
            with open('movie_top100.txt', 'a', encoding='utf-8') as w:
                w.write(movie_name + " " + movie_countries + " " + movie_time + " " + movie_grade + " \n")
                num += 1
                print(num)
