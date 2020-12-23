# _*_coding:UTF-8 _*_
import requests
import MySQLdb

url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php"
conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='spider',
    charset='utf8'
)
names = "赵钱孙李周吴郑王冯陈褚卫何吕施张"
cursor = conn.cursor()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
    'referer': 'https://www.baidu.com/s?wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&ie=utf-8&tn=78040160_5_pg&ch=2'
}
for name in names:
    sum_num = 0
    for page in range(0, 1010, 10):
        print("正在获取第{}页".format(int(page / 10 + 1)))
        params = {
            'resource_id': '6899',
            'query': '失信被执行人名单',
            'cardNum': '',
            'iname': name,
            'areaName': '',
            'pn': str(page),
            'rn': '10',
            'from_mid': '1',
            'ie': 'utf-8',
            'oe': 'utf-8',
            'format': 'json',
            't': '1601345031806',
            '_': '1601345005698',
        }
        res = requests.get(url,headers=headers,params=params).json()
        for data in res['data'][0]['disp_data']:
            sql = 'insert into loseman values(%s,%s)'
            # 往数据库里存储,案号作为主键,防止数据重复
            try:
                cursor.execute(sql,[data['caseCode'],data['iname']])
                conn.commit()
            except:
                sum_num += 1 #每重复一次报错一次
        if sum_num == 20:
            break

