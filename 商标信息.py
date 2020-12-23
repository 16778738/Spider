import MySQLdb
import requests

num = 1684
brand_num = 0
url = "http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearchDG.html"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}
# 1.连接数据库
conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    db='spider',
    charset='utf8'
)
cursor = conn.cursor()

for annnum in range(50):
    # 每一期进行创建一个表
    try:
        sql = 'create table brand{} (reg_num varchar(100) primary key,tmname varchar(100),reg_name varchar(100) )'.format(num)
        cursor.execute(sql)
        if cursor.fetchone():
            print("表{}创建成功".format(num))
    except:
        print("期号已存在")
    data = {
        'page': '1',
        'rows': '400000',
        'annNum': str(num),
        'annType': '',
        'tmType': '',
        'coowner': '',
        'recUserName': '',
        'allowUserName': '',
        'byAllowUserName': '',
        'appId': '',
        'appIdZhiquan': '',
        'bfchangedAgengedName': '',
        'changeLastName': '',
        'transferUserName': '',
        'acceptUserName': '',
        'regName': '',
        'tmName': '',
        'intCls': '',
        'fileType': '',
        'totalYOrN': 'true',
        'appDateBegin': '',
        'appDateEnd': '',
        'agentName': '',
    }
    # print(data)
    res = requests.post(url, data=data, headers=headers).json()

    for i in res['rows']:
        # print(i)
        try:
            # 2.准备sql语句
            sql = 'INSERT INTO brand{} VALUES(%s,%s,%s)'.format(num)
            # 3.执行sql
            cursor.execute(sql, [i['reg_num'], i['tm_name'], i['reg_name']])
            conn.commit()
            brand_num += 1
            print(brand_num)
        except Exception as e:
            print(f'存入数据失败，原因：{e}')
    num -= 1
    if brand_num == 10000000:
        break
