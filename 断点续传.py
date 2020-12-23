# _*_coding:UTF-8 _*_
import requests, MySQLdb
from lxml import etree

# 小说断点续传
conn = MySQLdb.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    db="spider",
    charset="utf8"
)
cursor = conn.cursor()


# 保存断点
def save_duan(book_url, cont_url, book_name):
    sql = "update duandian set book_url=%s,cha_url=%s,book_name=%s"
    cursor.execute(sql, [book_url, cont_url, book_name])
    conn.commit()


# 取断点
def get_duan():
    sql = 'select * from duandian'
    cursor.execute(sql)
    return cursor.fetchone()


# 获取所有书的url
def get_books_url():
    duan_book_url, cont_url, book_name = get_duan()
    url = "http://www.xbiquge.la/xiaoshuodaquan/"
    res = requests.get(url).text
    ele = etree.HTML(res)
    # 所有书的url
    book_urls = ele.xpath('//div[@id="main"]//li/a/@href')
    books_name_list = ele.xpath('//div[@id="main"]//li/a/text()')
    if duan_book_url == "1":  # 没断点
        for book_url in book_urls:
            book_name = books_name_list[book_urls.index(book_url)]
            get_chap_url(book_url, book_name)
    else:  # 有断点
        index = book_urls.index(duan_book_url)  # 获取索引值
        for book_url in book_urls[index:]:  # 从断点位置往下
            book_name = books_name_list[index]
            print(book_name)
            get_chap_url(book_url, cont_url, book_name)


# 获取每本书的章节url
def get_chap_url(book_url, cont_url=None, book_name=None):
    res = requests.get(book_url).content.decode("utf-8")
    ele = etree.HTML(res)
    chapter_urls = ele.xpath('//div[@id="list"]/dl/dd/a/@href')
    # 判断断点
    if cont_url:  # 有断点
        index = chapter_urls.index(cont_url)  # 获取章节索引值
        for chap_url in chapter_urls[index + 1:]:  # 从下一章开始抓取
            get_content(chap_url, book_url, book_name)
    else:
        for chap_url in chapter_urls:
            get_content(chap_url, book_url, book_name)


# 获取每章节的内容
def get_content(book_url, chap_url, book_name):
    res = requests.get("http://www.xbiquge.la" + chap_url).content.decode('utf-8')
    ele = etree.HTML(res)
    content = ele.xpath('//div[@id="content"]/text()')
    cha_name = ele.xpath('//h1/text()')[0]
    with open(str(book_name) + ".txt", "a", encoding="utf-8") as w:
        w.write(cha_name + "\n")
        for cont in content:
            w.write(cont)
        w.write("\n")
    save_duan(book_url, chap_url, book_name)  # 写入完毕保存断点


if __name__ == '__main__':
    get_books_url()
