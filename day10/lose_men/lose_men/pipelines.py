# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient
conn = MongoClient('mongodb://localhost:27017/')
db = conn.zfyMongo

class LoseMenPipeline:
    def process_item(self, item, spider):
        # print(item,type(item))
        # db.col.insert(dict(item))
        db.test.insert(dict(item))
        # db.col.createIndex(dict(item[gistId]), )

        return item
