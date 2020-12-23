# _*_coding:UTF-8 _*_
from pymongo import MongoClient

conn = MongoClient('mongodb://localhost:27017/')

db = conn.zfyMongo

db.col.insert({'name': 'TT'})

for item in db.col.find():
    print(item)

db.col.update('查询到的数据，修改的新值')

db.col.remove({'name': 'TT'})  # 删除这个文档（记录）
db.col.delete_one()  # 删除一个文档
db.col.delete_many()  # 删除多个文档  # 方法如果传入的是一个空的查询对象，则会删除集合中的所有文档：
db.col.drop()  # 删除这个集合（表）
