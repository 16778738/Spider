from lxml import etree
import pymysql, re, json, urllib.parse, time, requests
from random import randint, choice
import threading
from queue import Queue


class Lb_spider(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
            # 伪IP，完美解决本网站的反爬
            "X-Forwarded-For": str(randint(0, 255)) + "." + str(randint(0, 255)) + "." + str(randint(0, 255)) + "." + str(randint(0, 255))
        }

    def get_html(self, url):
        # 获取网页源代码的函数
        with requests.post(url, headers=self.headers) as rs:
            return rs.text

    def get_header(self):
        headers = {
            "User-Agent":  choice(
                [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
                    "Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50",
                    "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11"
                ]),
            # 伪ip，每次发请求的时候带上，这样的话每次请求的ip都不一样，适用于个别网站的反爬
            "X-Forwarded-For": str(randint(0, 255)) + "." + str(randint(0, 255)) + "." + str(randint(0, 255)) + "." + str(randint(0, 255))
        }
        return headers

    def parse(self, url):
        # 解析一级页面
        try:
            html = self.get_html(url)
            # print(html)
            response = etree.HTML(html)
            scripts = response.xpath('//body/script[3]/text()')[0]
            scr_str = str(scripts)
            # print(scr_str)
            # 利用正则匹配到需要的json字符串
            results = re.findall(re.compile(r''',"rows":(.*?)}'.*?'secondStatusColor''', re.S), scr_str)[0]
            json_str = json.loads(results)
            for json_ in json_str:
                # 商标状态
                status = json_['status']
                # 商标名称
                brandName = urllib.parse.unquote(json_['name'])
                # 详情页的参数token
                token = json_['token']
                # 商标号
                no = json_['code']
                # 申请人，json数据中是加密之后的数据，需要对其进行解密
                useName = urllib.parse.unquote(json_['proposerName'])
                # 申请地址
                addr = urllib.parse.unquote(json_['proposerAddress'])
                # 截止日期
                validEnd = json_['validEnd']
                if validEnd == '0':
                    teamEnd = ''
                else:
                    timeArray = time.localtime(int(validEnd))
                    teamEnd = time.strftime("%Y-%m-%d", timeArray)
                logo = json_['imageUrl']
                # 详情地址
                detail_href = f'https://www.biaoju01.com/trademark/detail/?token={token}'
                # print(status, brandName, no, useName, addr, logo, teamEnd, detail_href)
                self.parse_detail(status, brandName, no, useName, addr, logo, teamEnd, detail_href)
        except Exception as e:
            print(f'出错了，{e}')

    def parse_detail(self, status, brandName, no, useName, addr, logo, teamEnd, detail_href):
        headers = self.get_header()
        with requests.post(detail_href, headers=headers) as html:
            response = etree.HTML(html.text)
            scripts = response.xpath('//body/script[3]/text()')[0]
            scr_str = str(scripts)
            # 利用正则匹配到需要的json字符串
            results = re.findall(re.compile(r''''datas' :(.*?)'YIZHCHAN''', re.S), scr_str)[0].split("parseJSON(\'")[-1].split("\'),")[0]
            json_str = json.loads(str(results))
            # 国家分类
            cid = json_str['classId']
            # 商标状态
            if '申请中' in status:
                status = 3
            elif '商标已无效' in status:
                status = 1
            elif '已注册' in status:
                status = 4
            else:
                status = 2
            # 申请日期，拿下来的是时间戳，需要进行转换
            applyDate = json_str['applyDate']
            timeArray = time.localtime(int(applyDate))
            startDate = time.strftime("%Y-%m-%d", timeArray)
            # 注册日期
            validStart = json_str['validStart']
            if validStart == '0':
                termStart = ''
            else:
                timeArray = time.localtime(int(validStart))
                termStart = time.strftime("%Y-%m-%d", timeArray)
            print(brandName, no, startDate, cid, useName, logo, addr, status, termStart, teamEnd)
            # self.save_data(brandName, no, startDate, cid, useName, logo, addr, status, termStart, teamEnd)

    def save_data(self, *args):
        """保存数据"""
        print(args)
        # 1.连接数据库
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            db='spider',
            charset='utf8'
        )
        cursor = conn.cursor()
        # 商标的注册号是唯一的，所以根据这个字段进行去重
        # 先查询数据库中是否存在这个数据，如果存在就不存，如果不存在就更新数据库，
        select = f'''select count(*) from fanxiang_company_mark where no="{args[1]}" and cid="{args[3]}"'''
        print(select)
        cursor.execute(select)
        # rows:查询到的符合条件的个数，如果为0，说明数据库里不存在，则进行存数据库操作；否则不存数据库
        rows = cursor.fetchone()
        if rows[0] == 0:
            # 不存在，开始进行存入数据库操作
            try:
                print(f'正在存入注册号为<{args[1]}>的<{args[0]}>下的数据，请稍等...')
                # 2.准备sql语句
                sql = """INSERT IGNORE INTO fanxiang_company_mark(brandName, no, startDate, cid, useName, logo, addr, status, termStart, teamEnd)VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % args
                # 3.执行sql
                cursor.execute(sql)
                conn.commit()
                print(f'<{args[0]}>下的数据入库成功~~~')
                print('*'*80)
            except Exception as e:
                print(f'存入数据失败，原因：{e}')
                print('*' * 80)
            finally:
                # 最好执行一次数据库操作，关闭一次，否则的话sql语句过多会导致数据库异常报错
                conn.close()
        else:
            # 数据已存在，无需进行存数据库操作
            print('数据已存在！！！')
            print('*'*80)

    def run(self, name_quequ):
        while not name_quequ.empty():
            key = name_quequ.get()
            url = f'https://www.biaoju01.com/statusquery/index/?keyword={key}&classId=&statusId=&agentName=&startNumber=&endNumber=&timeType=&startTime=&endTime=&showType=img&searchType=state&page=1'
            html = self.get_html(url)
            response = etree.HTML(html)
            name = re.findall(re.compile(r'<title>(.*?) - 商标', re.S), html)[0]
            print(name)
            try:
                scripts = response.xpath('//body/script[3]/text()')[0]
                scr_str = str(scripts)
                results1 = ''.join(scr_str).split('span')[1]
                # 总页数
                total_page = re.findall(re.compile(r'共(.*?)页', re.S), results1)[0]
                total_num = re.findall(re.compile(r'"total":(.*?),"rows', re.S), scr_str)[0]
                print(f'该分类下有{total_page}页，共{total_num}条数据！！')
                if int(total_page) > 1:
                    for x in range(1, int(total_page) + 1):
                        # 拼接下一页链接
                        next_page_href = url.replace('&page=1', f'&page={x}')
                        print(f'正在爬取第{x}页数据，网址为：{next_page_href}')
                        headers = self.get_header()
                        with requests.post(next_page_href, headers=headers) as html:
                            url = next_page_href
                            # self.get_html(next_page_href)
                            self.parse(url)
                            print(f'第{x}页数据爬取结束！')
                            print('-' * 100)
                elif int(total_page) == 1:
                    print(f'网址为：{url}')
                    # self.get_html(url)
                    self.parse(url)
                    print('没有下一页了~~~')
                    print('-' * 100)
            except Exception as e:
                print('该分类下没有相同数据~~~')
                print('-' * 100)


if __name__ == '__main__':
    lb = Lb_spider()
    name_quequ = Queue()
    name_list = ['梁小猴港式铁板炒饭', '爱必喜披萨', '一蘭拉面', '杨国福麻辣烫', '绝味鸭脖', '大牌冒菜', '妯娌老鸭粉丝汤', '香锅里辣麻辣香锅', '华莱士', '张亮麻辣烫', '顾一碗', '东池便当', '巴比馒头', '快客便利店', '1号便当', '吉祥馄饨', '三米粥铺']
    threads = []
    for brandname in name_list:
        key = urllib.parse.quote(brandname)
        # 把品牌名称遍历，放进队列里
        name_quequ.put(brandname)
    for i in range(21):
        # 开启线程20个线程，参数：线程函数为Thread_main，并且线程函数里边的参数为品牌队列brand_name_quequ
        t = threading.Thread(target=lb.run, args=(name_quequ,))
        # 添加线程至列表
        threads.append(t)
    for x in threads:
        # 开启线程
        x.start()
    for x in threads:
        x.join()