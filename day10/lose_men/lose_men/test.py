# _*_coding:UTF-8 _*_
from pymongo import MongoClient

conn = MongoClient('mongodb://localgost:27017/')

db = conn.zfyMongo
db.test.find()