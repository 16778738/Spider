import re

import scrapy
from Spider.day11.stock.stock.items import StockItem

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Referer': 'http://quote.eastmoney.com/'
}
body = {
    'cb': 'jQuery11240854165108655986_1602673187549',
    'pn': '1',
    'pz': '20',
    'po': '1',
    'np': '1',
    'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
    'fltt': '2',
    'invt': '2',
    'fid': 'f3',
    'fs': 'm:105,m:106,m:107',
    'fields': ' f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152',
    '_': ' 1602673187600',
}
cookie = {
    "qgqp_b_id": "25122f88619c1074bcfd0f4ecd38a21c", " st_si": "52299067089418", " st_asi": "delete",
    " st_pvi": "34253320877179", " st_sp": "2020-10-14%2016%3A59%3A13",
    " st_inirUrl": "http%3A%2F%2Fquote.eastmoney.com%2Fcenter%2Fgridlist.html", " st_sn": "3",
    " st_psi": "20201014185948512-113200301321-3068650977"
}


class GupiaoSpider(scrapy.Spider):
    name = 'gupiao'

    def start_requests(self):
        for i in range(1, 479):
            # url = "http://41.push2.eastmoney.com/api/qt/clist/get?"
            url = "http://41.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240854165108655986_1602673187549&pn={}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:105,m:106,m:107&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152&_=1602673187600".format(
                i)
            # yield scrapy.Request(url, headers=headers,body=json.dumps(body))
            yield scrapy.Request(url, headers=headers, )

    def parse(self, response):
        # print(response.text)
        name_rule = '"f14":"(.*?)"'
        price_limit_rule = '"f3":(.*?),'
        up_down_rule = '"f4":(.*?),'
        now_price_rule = '"f2":(.*?),'

        name_code = "没有操作权限"
        name = re.findall(name_rule, response.text)
        now_price = re.findall(now_price_rule, response.text)
        up_down = re.findall(up_down_rule, response.text)
        price_limit = re.findall(price_limit_rule, response.text)
        for i in name:
            index = name.index(i)
            item = StockItem()
            item['name_code'] = name_code
            item['name'] = name[index]
            item['now_price'] = now_price[index]
            item['up_down'] = up_down[index]
            item['price_limit'] = price_limit[index]
            yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'gupiao'])
