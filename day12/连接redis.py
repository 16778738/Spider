# _*_coding:UTF-8 _*_
import json

from redis import Redis

red = Redis(host='127.0.0.1', port=6379)
# res = red.lrange('hehe',0,-1)
# for n in res:
#     print(n)
res = red.get('zfy')
print(res)