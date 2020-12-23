# _*_coding:UTF-8 _*_
from pymongo import MongoClient
conn = MongoClient('mongodb://localhost:27017/')
db = conn.zfyMongo

for i in db.col.find({"name":"高惠媛"}):
    print(i)