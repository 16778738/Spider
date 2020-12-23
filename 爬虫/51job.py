# _*_coding:UTF-8 _*_
import json
import re
from urllib import request

for i in range(1, 6):
    url = "https://search.51job.com/list/010000,000000,0000,00,9,99,%25E9%2594%2580%25E5%2594%25AE,2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=".format(
        i)
    res = request.urlopen(url).read().decode('gbk')
    # 因为数据存放在script中,json数据 使用json.loads解序列化;json.dumps序列化
    rule = '__SEARCH_RESULT__ = (.*?)</script>'
    job_dict = json.loads(re.findall(rule, res)[0])
    for job in job_dict['engine_search_result']:
        if not job['providesalary_text']:
            job['providesalary_text'] = "面议"
        print(job['job_name'], job['providesalary_text'])
