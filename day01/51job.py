# _*_coding:UTF-8 _*_

# from urllib import request
# import gzip
# from lxml import etree
# import re
# import requests
#
#
# def get_proxy():
#     return requests.get("http://127.0.0.1:5010/get/").json()
#
#
# def delete_proxy(proxy):
#     requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
#
#
# def getHtml():
#     retry_count = 5
#     proxy = get_proxy().get("proxy")
#     while retry_count > 0:
#         try:
#             html = requests.get('http://www.66ip.cn/', proxies={"http": "http://{}".format(proxy)})
#             # 使用代理访问
#             return html
#         except Exception:
#             retry_count -= 1
#     # 删除代理池中代理
#     delete_proxy(proxy)
#     return None
#
#
# num = 0
# for pn in range(710, 1462):
#     url = "https://search.51job.com/list/000000,000000,0000,00,9,99,java,2,{}.html".format(pn)
#     headers = {
#         'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20101101 Firefox/6.0",
#         'referer': 'url'}
#
#     # 'user-agent': "baiduSpider"}
#     req = request.Request(url)
#     res = request.urlopen(req).read()
#     try:
#         res = gzip.decompress(res).decode('gbk')
#     except:
#         res = res.decode('gbk')
#
#     rule = '"job_href":"(.*?)"'
#     job_url_list = re.findall(rule, res)
#     for i in job_url_list:
#         a = i.replace("\\/", "/")
#         req = request.Request(a, headers=headers)
#         job_url = request.urlopen(req).read()
#         try:
#             try:
#                 job_url_result = job_url.decode('gbk')
#             except:
#                 job_url_result = gzip.decompress(job_url).decode('gbk')
#
#             ele = etree.HTML(job_url_result)
#             job_name = ele.xpath('//h1/text()')[0]
#             job_company = ele.xpath('//div[@class="cn"]/p[@class="cname"]/a[@class="catn"]/text()')[0]
#             try:
#                 job_salary = ele.xpath('//div[@class="cn"]/strong/text()')[0]
#             except:
#                 job_salary = "面议"
#             job_place = ele.xpath('//div[@class="cn"]/p[@class="msg ltype"]/text()')[0]
#         except:
#             print("没有此职位")
#         with open('51job.txt', 'a', encoding='utf-8') as w:
#             w.write(job_name + " " + job_company + " " + job_salary + " " + job_place + " " + "\n")
#             num += 1
#             print(num)
#

import gzip
import re
from urllib import request

num = 0
for pn in range(1, 1462):
    url = "https://search.51job.com/list/000000,000000,0000,00,9,99,java,2,{}.html".format(pn)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20101101 Firefox/6.0",
        'referer': 'url'}
    # 'user-agent': "baiduSpider"}
    req = request.Request(url)
    res = request.urlopen(req).read()
    try:
        res = gzip.decompress(res).decode('gbk')
    except:
        res = res.decode('gbk')
    jpb_name_rule = '"job_title":"(.*?)"'
    jpb_conmoany_rule = '"company_name":"(.*?)"'
    jpb_salary_rule = '"providesalary_text":"(.*?)"'
    jpb_place_rule = '"workarea_text":"(.*?)"'

    job_names = re.findall(jpb_name_rule, res)
    job_company = re.findall(jpb_conmoany_rule, res)
    job_salary = re.findall(jpb_salary_rule, res)
    job_place = re.findall(jpb_place_rule, res)

    with open('51job.txt', 'a', encoding='utf-8') as w:
        for job_name in job_names:
            index = job_name.index(job_name)
            w.write(job_name + " " + job_company[index] + " " + job_salary[index] + " " + job_place[index] + " " + "\n")
            num += 1
            if num == 50000:
                break
            print(num)
