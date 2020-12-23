import json
import re

import scrapy
# from ..items import LearnItem


class JobSpider(scrapy.Spider):
    name = 'job'
    # allowed_domains = ['job.com']
    start_urls = ['http://www.baidu.com/']

    def start_requests(self):
        for i in range(1, 100):
            url = "https://search.51job.com/list/010000,000000,0000,00,9,99,%25E9%2594%2580%25E5%2594%25AE,2,{}.html?".format(i)
            yield scrapy.Request(url)

    def parse(self, response):
        # print(response.text)
        # # print(response.xpath('//title/text()').extract())
        # print(response.xpath('//title/text()').getall())
        rule = '__SEARCH_RESULT__ = (.*?)</script>'
        job_dict = json.loads(re.findall(rule, response.text)[0])
        for job in job_dict['engine_search_result']:
            yield scrapy.Request(job['job_href'], callback=self.parse1)

    def parse1(self, res):
        print(res)
        # con_name = res.xpath('')
        # job_name = res.xpath('')
        # item = LearnItem()
        # item['com_names'] = con_name
        # item['job_names'] = job_name


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'job'])
