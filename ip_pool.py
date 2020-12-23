# _*_coding:UTF-8 _*
import random

import requests
import MySQLdb
from multiprocessing import Pool as P
# 定义代理池
from lxml import etree


class DB:
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='spider',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    # 存IP
    def save(self, ip):
        sql = "insert into ip_pool values(%s)"
        self.cursor.execute(sql, [ip])
        self.conn.commit()

    # 取一条IP
    def get_ip(self):
        return self.get_all_ip()[0]

    # 取所有IP
    def get_all_ip(self):
        sql = "select * from ip_pool"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 删IP
    def delete_ip(self, ip):
        sql = 'delete from ip_pool where ip=%s'
        self.cursor.execute(sql, [ip])
        self.conn.commit()

    # 提供数量
    def get_count(self):
        return len(self.get_all_ip())

    def close(self):
        self.cursor.close()
        self.conn.close()


# 操作池,也是对外的接口
class Pool:
    def __init__(self, limit):
        self.db = DB()  # 实例池
        self.limit = limit  # 设定池的阈值
        self.local_ip = requests.get("http://httpbin.org/ip").text

    def __new__(cls, limit):
        if isinstance(limit, int):
            return super().__new__(cls)

    def crawl_ip(self):
        if self.db.get_count() < self.limit:
            for page in range(1, 50):
                url = "http://www.nimadaili.com/https/%s/" % page
                res = requests.get(url).content.decode('utf-8')
                ele = etree.HTML(res)
                # 匹配IP
                ips = ele.xpath('//tbody/tr/td[1]/text()')
                for ip in ips:
                    dict1 = {}
                    dict1['https'] = "https://"+ip
                    # print("开始测试{}".format(dict1))
                    # 如果通过测试可用,则存储
                    try:
                        if self.check_ip(dict1):
                            print("代理可用:%s" % dict1)
                            self.db.save(str(dict1))
                    except:
                        print("{}代理已存在".format(dict1))
                    if self.db.get_count() == self.limit:
                        return
            self.db.close()

    # 检测IP是否可用
    def check_ip(self, ip):
        try:
            target = requests.get("https://httpbin.org/ip", proxies=ip).text
            if self.local_ip != target:
                return True
        except:
            pass

    # 全部检测
    def check_all_ip(self):
        for ip in self.db.get_all_ip():
            print("检测ip:{}".format(eval(ip[0])))
            # 遍历出来的ip,未通过检测,则删除
            if not self.check_ip(eval(ip[0])):
                self.db.delete_ip(ip[0])
                print("ip不可用")

    # 抽样检测
    def check_many_ip(self, num):
        choice = random.sample(self.db.get_all_ip(), num)
        for ip in choice:
            print("检测ip:{}".format(eval(ip[0])))
            # 遍历出来的ip,未通过检测,则删除
            if not self.check_ip(eval(ip[0])):
                self.db.delete_ip(ip[0])
                print("ip不可用")

    # 对外提供可用IP
    def offer_all_ip(self):
        ips = self.db.get_all_ip()
        return ips

    # 对外提供一条ip
    def offer_ip(self):
        ip = self.db.get_ip()[0]
        self.db.delete_ip(ip)  # 提取一条删除一条
        return eval(ip)  # 对外提供直接可用的ip


if __name__ == '__main__':
    pool = Pool(100)
    pool.check_all_ip()
    pool.crawl_ip()

