# _*_coding:UTF-8 _*_
from urllib import request, parse

from http import cookiejar  # 用户保存在请求的过程中的响应cookie值


# 封装类
class urlreq(object):
    # 初始化,初始化opener
    def __init__(self):
        # 通过对象创建cookie
        cookie_ob = cookiejar.CookieJar()
        # 实例化对应的cookie进行操作的handler
        handler = request.HTTPCookieProcessor(cookie_ob)
        # 获取opener请求对象绑定cookie对应的handler
        self.opener = request.build_opener(handler)

    # 对象get函数
    def get(self, url, headers=None):
        return get(url, headers=headers, opener=self.opener)

    # 对象post函数
    def post(self, url, form, headers=None):
        return post(url, form, headers=headers, opener=self.opener)


# 封装get请求
def get(url, headers=None, opener=None):
    return urlrequests(url, headers=headers, opener=opener)


# 封装post请求
def post(url, form=None, headers=None, opener=None):
    return urlrequests(url, form, headers=headers, opener=opener)


# 封装request网络请求
def urlrequests(url, form=None, headers=None, opener=None):
    # 请求头
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    if not headers:
        headers = {
            'User-Agent': user_agent
        }
    html_byte = b''
    try:
        if form:
            # post
            # 对form数据进行urlencode编码
            form_str = parse.urlencode(form)
            # 将编码后对form数据转换为bytes类型
            form_byte = form_str.encode('utf-8')
            req = request.Request(url, data=form_byte, headers=headers)
        else:
            # get
            req = request.Request(url, headers=headers)
        # 判断是否提供opener,如提供了则通过opener发送请求并获取返回response
        if opener:
            response = opener.open(req)
        else:
            response = request.urlopen(req)

        html_byte = response.read()
    except:
        pass
