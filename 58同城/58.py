# _*_coding:UTF-8 _*_
import requests
import time
import pymysql
from lxml import etree
from Spider.ip_pool import Pool

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

ips = Pool(10)


# proxy = ips.offer_ip()
# print(proxy)

# 提取租房信息
def parse_pages(pages):
    num = 0
    ele = etree.HTML(pages)
    try:
        city = ele.xpath('//head/title/text()')[0].split('-')[1][:-4]
        title = ele.xpath('//h2/a/text()')
        print(len(title))
        sum_price = ele.xpath("//div[@class='price']/p[@class='sum']/b/text()")
        evey_price = ele.xpath("//div[@class='price']/p[@class='unit']/text()")
    except:
        time.sleep(60 * 5)
        print("出现验证码,5分钟后操作")
        city = ele.xpath('//head/title/text()')[0].split('-')[1][:-4]
        title = ele.xpath('//h2/a/text()')
        print(len(title))
        sum_price = ele.xpath("//div[@class='price']/p[@class='sum']/b/text()")
        evey_price = ele.xpath("//div[@class='price']/p[@class='unit']/text()")
    for i in title:
        index = title.index(i)
        try:
            data = [title[index].split('\/xa0')[0], sum_price[index] + '万', evey_price[index], city]
            num += 1
            save_to_mysql(data)
            print('第' + str(num) + '条数据爬取完毕，暂停1.5秒！')
            time.sleep(1.5)
        except Exception as e:
            print(e)


# 创建MySQL数据库的表：58tc_data
def create_mysql_table():
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spider')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS 58tc_xinfang (title VARCHAR(100) PRIMARY KEY,sum_price VARCHAR(255), every_price VARCHAR(100) ,city VARCHAR(255) )'
    cursor.execute(sql)
    db.close()


# 将数据储存到MySQL数据库
def save_to_mysql(data):
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spider')
    cursor = db.cursor()
    sql = 'INSERT INTO 58tc_xinfang(title,sum_price,every_price,city) values(%s, %s, %s, %s)'
    try:
        cursor.execute(sql, (data[0], data[1], data[2], data[3]))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()


if __name__ == '__main__':
    # create_mysql_table()
    # print('MySQL表58tc_xifang创建成功！')
    city_list = ['fs', 'gz', 'zz', 'dg', 'sh', 'bj', 'nj', 'dl', 'tj', 'nb', 'cd', 'wx', 'hz', 'wh', 'sy', 'sz', 'xa',
                 'cq', 'cs', 'qd']
    for city in city_list:
        for i in range(20, 25):
            url = ('https://{}.58.com/ershoufang/pn' + str(i) + '/').format(city)
            print(url)
            pro_pages = requests.get(url).text
            parse_pages(pro_pages)
            print('第' + str(i) + '页数据爬取完毕！')
            # time.sleep(random.randint(3, 10))
        print('所有数据爬取完毕！')
