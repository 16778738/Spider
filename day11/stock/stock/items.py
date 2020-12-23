# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    name_code = scrapy.Field()
    now_price = scrapy.Field()  # 最新价(美元)
    up_down = scrapy.Field()  # 涨跌额
    price_limit = scrapy.Field()  # 涨跌幅
