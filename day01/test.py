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
    # print(res)
    jpb_name_rule = '"job_title":"(.*?)"'
    jpb_conmoany_rule = '"company_name":"(.*?)"'
    jpb_salary_rule = '"providesalary_text":"(.*?)"'
    jpb_place_rule = '"workarea_text":"(.*?)"'

    job_names = re.findall(jpb_name_rule,res)
    job_company = re.findall(jpb_conmoany_rule,res)
    job_salary = re.findall(jpb_salary_rule,res)
    job_place = re.findall(jpb_place_rule,res)
    # print(job_name)
    with open('51job.txt', 'a', encoding='utf-8') as w:
        for job_name in job_names:
            index = job_name.index(job_name)
            w.write(job_name + " " + job_company[index] + " " + job_salary[index]+ " " + job_place[index] + " " + "\n")
            num += 1
            if num == 50000:
                break
            print(num)

