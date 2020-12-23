# _*_coding:UTF-8 _*_
import MySQLdb
from pyecharts import options
from pyecharts.charts import Bar, Pie, Page
from pyecharts.globals import ThemeType

city_list = ['北京', '天津', '青岛', '武汉', '长沙', '重庆', '西安', '深圳', '沈阳', '杭州', '成都', '大连', '上海', '南京', '东莞', '广州', '佛山', '无锡',
             '郑州']


def select_average_price():
    average_list = []
    conn = MySQLdb.connect(host='localhost', user='root', password='123456', port=3306, db='spider', charset='utf8')
    cursor = conn.cursor()
    for city in city_list:
        sql = 'select price from 58tc_zufang where city="{}"'.format(city)
        cursor.execute(sql)
        price_list = cursor.fetchall()
        sum_price = 0
        number = len(price_list)
        for price in price_list:
            sum_price += int(price[0].replace('元/月', ''))
        average = sum_price / number  # 5837.533109807208
        average_list.append(format(average, '.2f'))
    return average_list


price_list = select_average_price()
# 柱状图
bar_obj = (
    Bar(init_opts=options.InitOpts(theme=ThemeType.MACARONS)) \
        .add_xaxis((city_list)) \
        .add_yaxis("", price_list) \
        .set_global_opts(title_opts=options.TitleOpts("租房平均价格元/月", subtitle='仅供参考'),
                         toolbox_opts=options.ToolboxOpts(),  # 工具栏选项
                         brush_opts=options.BrushOpts()  # 工具刷对象
                         )
)

# 饼状图
b_list = [list(i) for i in zip(city_list, price_list)]
pie_ogj = (
    Pie()
        .add("", b_list)
        .set_series_opts(label_opts=options.LabelOpts(formatter="{b}: {c}"))
)
# page对象用于整合地图
p = Page(layout=Page.SimplePageLayout)
p.add(pie_ogj, bar_obj)
p.render("一线城市租房信息整合.html")
