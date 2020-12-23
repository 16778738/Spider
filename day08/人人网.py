import requests
from lxml import etree
import MySQLdb

conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='spider',
    charset='utf8'
)
cursor = conn.cursor()
cookies = {'t': '3d0a10d3475579d459b942e80d5f84c64'}


# 存储namecard
def save_id(ids, name1):
    for namecard in ids:
        index = ids.index(namecard)
        try:
            sql = 'insert into renren_card values(%s,%s,%s)'
            # sql1 = 'insert into renren_card1 varchar(%s,%s,%s) '
            cursor.execute(sql, [namecard, '0', name1[index].split(' ')[0]])  # 存储的card状态为未爬取
            # cursor.execute(sql1, [namecard, '0', job_place])  # 存储的card状态为未爬取
            conn.commit()
        except:
            pass


# 修改状态
def change_flag(name_card):
    sql = 'update renren_card set flag=1 where namecard=%s'
    cursor.execute(sql, [name_card])
    conn.commit()


# 提取namecard
def get_name_card():
    sql = 'select namecard from renren_card where flag=%s'
    cursor.execute(sql, ["0"])  # 提取状态为未爬取的数据
    get_content(cursor.fetchone()[0])  # 返回namecard字符串


# 获取数据
def get_content(name_card):
    res = requests.get("http://www.renren.com/" + name_card + "/profile", cookies=cookies).text
    change_flag(name_card)  # 提取的namecard修改状态为已爬取
    # 获取关联用户
    ele = etree.HTML(res)
    name = ele.xpath('//title/text()')
    print(name)
    # job_place = ele.xpath('//div[@class="tl-information"]/ul/li[@class="work"]/span/@title')
    # print(job_place)
    name1 = ele.xpath('//div[@id="footprint-box"]/ul/li/span[@class="time-tip"]/span[@class="tip-content"]/text()')
    namecards = ele.xpath('//div[@id="footprint-box"]/ul/li/a/@namecard')
    # save_id(namecards, name1,job_place)
    save_id(namecards, name1)


while True:
    get_name_card()
