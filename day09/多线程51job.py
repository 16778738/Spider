# _*_coding:UTF-8 _*_
from multiprocessing import Pool  # 进程池
import requests
import json
import re
from concurrent.futures import ThreadPoolExecutor
# from concurrent.futures import ProcessPoolExecutor  # 进程池


# 多进程爬取
def run(page):
    print("开始爬取")
    for i in range(1, page):
        url = "https://search.51job.com/list/010000,000000,0000,00,9,99,%25E9%2594%2580%25E5%2594%25AE,2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=".format(
            i)
        res = requests.get(url, headers={'user-agent': "baiduspider"}).text
        rule = '__SEARCH_RESULT__ = (.*?)</script>'
        job_dict = json.loads(re.findall(rule, res)[0])
        for job in job_dict['engine_search_result']:
            if not job['providesalary_text']:
                job['providesalary_text'] = "面议"
            print(job['job_name'], job['providesalary_text'])


if __name__ == '__main__':
    pool = Pool(10)
    for i in range(100):
        pool.apply_async(run, (i,))
    pool.close()
    pool.join()
    print("爬取结束")


# 多线程爬取
def run(url):
    print("开始爬取")
    res = requests.get(url, headers={'user-agent': "baiduspider"}).text
    rule = '__SEARCH_RESULT__ = (.*?)</script>'
    job_dict = json.loads(re.findall(rule, res)[0])
    for job in job_dict['engine_search_result']:
        if not job['providesalary_text']:
            job['providesalary_text'] = "面议"
        print(job['job_name'], job['providesalary_text'])


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=10)
    for i in range(1, 1000):
        url = "https://search.51job.com/list/010000,000000,0000,00,9,99,%25E9%2594%2580%25E5%2594%25AE,2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=".format(
            i)
        pool.submit(run, url)

# import requests
# from multiprocessing import Pool  #进程池
# import threading
# import os
# #1 - 625
# def run(i):
#     print("开始")
#     url = "https://douban.donghongzuida.com/20201009/10722_a9c63d95/1000k/hls/a02ef2edf7d000%03d.ts"%i
#     r = requests.get(url).content
#     name = url[-7:]
#     print("开始下载:%s"%name)
#     # with open("movie/{}".format(name),'wb') as w:
#     #     w.write(r)
# if __name__ == '__main__':
#     pool = Pool(10)
#     for i in range(1,625):
#         pool.apply_async(run,args=(i,))
#     pool.close()
#     pool.join()
#     print("爬虫结束")
#     # a = os.popen('copy /b .\movie\*.ts hehe.mp4')
#     # print(a.read())
