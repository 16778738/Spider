import re

import scrapy
from Spider.day13.baidutieba.baidutieba.items import BaidutiebaItem
from Spider.ip_pool import Pool
ips = Pool(10)
ip = ips.offer_ip()

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    # allowed_domains = ['baidu.com']
    # start_urls = ['http://baidu.com/']

    def start_requests(self):
        tieba_name = ['NBA', '李毅','英雄联盟',]
        for tie_name in tieba_name:
            for page in range(1,100):
                url = "https://tieba.baidu.com/f?ie=utf-8&kw="+str(tie_name)+" &pn={}&".format(page)
                yield scrapy.Request(url)

    def parse(self, response):
        title = response.xpath('//head/title/text()').getall().split('-')[0]
        print(title,response.text)
        name_rule = 'title="主题作者: (.*?)"'
        name = re.findall(name_rule, response.text)
        content_list = response.xpath('//div[@class="threadlist_abs threadlist_abs_onlyline "]/text()').getall()
        for i in content_list:
            index = content_list.index(i)
            content = i.strip().replace('\n', '')
            item = BaidutiebaItem()
            item['title'] = title
            item['name'] = name[index]
            item['content'] = content
            yield item


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scray', 'crawl', 'baidu'])
