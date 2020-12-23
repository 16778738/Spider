# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# from pymongo import MongoClient
# conn = MongoClient('mongodb://localhost:27017/')
# db =conn.zfyMongo

import MySQLdb
conn =MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='spider',
    charset='utf8'
)
cursor =conn.cursor()
sql = "insert into baidutieba values (%s,%s,%s)"

class BaidutiebaPipeline:
    def process_item(self, item, spider):
        # db.baidutieba1.insert(dict(item))
        # print(item['name'],item['content'])
        cursor.execute(sql,[item['name'],item['content'],item['title']])
        conn.commit()
        return item
