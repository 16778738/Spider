# _*_coding:UTF-8 _*_
import re
import traceback
import requests
from Spider import ip_pool
from lxml import etree


num = 0
url = "https://www.cnvd.org.cn/flaw/list.htm?flag="
headers = {
    # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "referer": "https://www.cnvd.org.cn/flaw/list.htm?flag=",
    # "Cookie": "__jsluid_s=5cb18648cabd2a98d2d298992da255fe; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1601376686; __jsl_clearance_s=1601422209.994|0|nwd0VZWeGxyy9vRwvL3aTMlG178%3D; JSESSIONID=6D478B41A4823006460AB9A0A5F302A1"
}
for page in range(10002,148523,20):
    params ={
        "offset": str(page)
    }
    try:
        res = requests.post(url,headers=headers, data=params,  timeout=3).text
        # print(res)
        ele = etree.HTML(res)
        urls_list_rule = ''
        urls_list = ele.xpath('//div[@id="flawList"]/tbody/tr/td/a/@href')
        # print(urls_list)
        # 拼接url
        url_list = ["https://www.cnvd.org.cn" + url for url in urls_list]
        # print(url_list)

        for bug_url in url_list:
            bug_details_rule = '漏洞描述</td>(.*?)</td>'
            bug_affect_rule = '影响产品</td>(.*?)</td>'
            bug_solve_rule = '漏洞解决方案</td>(.*?)</td>'
            title = '<h1 >(.*?)</h1>'
            print(bug_url)
            try:
                res1 = requests.post(bug_url, headers=headers).text
                bug_name = re.findall(title, res1, re.S)[0]
                bug_details = re.findall(bug_details_rule, res1, re.S)[0].replace('<td>','').replace('\n','').replace('\t','').replace('\r','').replace('<br/>','')
                bug_affect = re.findall(bug_affect_rule, res1, re.S)[0].replace('<td>','').replace('\n','').replace('\t','').replace('\r','').replace('<br/>','')
                bug_solve = re.findall(bug_solve_rule, res1, re.S)[0].replace('<td>','').replace('\n','').replace('\t','').replace('\r','').replace('<br/>','')
                with open("漏洞采集.txt","a", encoding='utf-8') as w:
                    w.write("漏洞名称:"+str(bug_name)+" "+"漏洞描述"+str(bug_details)+" "+"漏洞影响"+str(bug_affect)+" "+"解决方案"+str(bug_solve)+" "+"\n")
                    num += 1
                    print(num)
            except:
                pass
    except:
        pass
    if num ==5000:
        break

