# _*_coding:UTF-8 _*_
from pyecharts.charts import Bar, Pie, Map, Page
from pyecharts import options
from pyecharts.globals import ThemeType

# bar = Bar()
# bar.add_xaxis(('a', 'b', 'c'))
# bar.add_yaxis("A",[1,2,3])
# bar.render()

# Bar(init_opts=options.InitOpts(theme=ThemeType.MACARONS)).add_xaxis(("衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子")) \
#     .add_yaxis("商家A", [5, 20, 36, 10, 75, 90]) \
#     .add_yaxis("商家B", [10, 10, 56, 20, 75, 80]) \
#     .set_global_opts(title_opts=options.TitleOpts("衣服销量",subtitle='仅供参考'),
#                      toolbox_opts=options.ToolboxOpts(), #工具栏选项
#                      brush_opts=options.BrushOpts() #工具刷对象
#                      ) \
#     .render("1.html")

# pie_ogj = (
#     Pie()
#         .add("数据", [["北京",200],["吉林",300],["山西",800],["广东",500]])
#         .set_global_opts(title_opts=options.TitleOpts(title="Pie-基本示例"))
#         .set_series_opts(label_opts=options.LabelOpts(formatter="{b}: {c}"))
#         .render("pie_base.html")
# )
# map_obj = (
#     Map()
#         .add("商家A", [["北京",200],["吉林",300],["山西",800],["广东",500]], "china")
#         .set_global_opts(
#         title_opts=options.TitleOpts(title="Map-VisualMap（连续型）"),
#         visualmap_opts=options.VisualMapOpts(max_=600),
#     ).render('地图.html')
# )

pie_obj = (
    Pie()
        .add("数据", [["北京",200],["吉林",300],["山西",800],["广东",500]])
        .set_global_opts(title_opts=options.TitleOpts(title="Pie-基本示例"))
        .set_series_opts(label_opts=options.LabelOpts(formatter="{b}: {c}"))
)
map_obj = (
    Map()
        .add("商家A", [["北京",200],["吉林",300],["山西",800],["广东",500]], "china")
        .set_global_opts(
        title_opts=options.TitleOpts(title="Map-VisualMap（连续型）"),
        visualmap_opts=options.VisualMapOpts(max_=600),
    )
)
# page对象用于整合地图
p = Page(layout=Page.SimplePageLayout)
p.add(pie_obj,map_obj)
p.render("地图整合.html")


