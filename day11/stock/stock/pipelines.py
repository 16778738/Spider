# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import MySQLdb
conn =MySQLdb.connect(
    host='192.168.10.106',
    port=3306,
    user='zfy',
    passwd='123456',
    db='public_db',
    charset='utf8'
)
cursor =conn.cursor()
sql = "insert into zfy_gupiao values (%s,%s,%s,%s,%s)"

# from pymongo import MongoClient
# conn = MongoClient('mongodb://localhost:27017/')
# db = conn.zfyMongo
class StockPipeline:
    def process_item(self, item, spider):
        print(item)
        cursor.execute(sql,[item['name'],item['name_code'],item['now_price'],item['price_limit'],item['up_down']])
        conn.commit()
        # db.gupiao.insert(dict(item))
        return item
