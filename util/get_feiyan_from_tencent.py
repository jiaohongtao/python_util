import json

import pandas as pd
import requests

from pyecharts.charts import *  # 导入所有图表
from pyecharts import options as opts
# 导入pyecharts的主题（如果不使用可以跳过）
from pyecharts.globals import ThemeType

"""
源教程地址：https://blog.csdn.net/weixin_43130164/article/details/104113559
"""


def catch_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    reponse = requests.get(url=url).json()
    # 返回数据字典
    return json.loads(reponse['data'])


data = catch_data()
# print(data.keys())

# 数据集包括["国内总量","国内新增","更新时间","数据明细","每日数据","每日新增"]
lastUpdateTime = data['lastUpdateTime']
chinaTotal = data['chinaTotal']
chinaAdd = data['chinaAdd']
# print(lastUpdateTime)
# print(chinaTotal)
# print(chinaAdd)

# 数据明细，数据结构比较复杂，一步一步打印出来看，先明白数据结构
areaTree = data['areaTree']
# 国内数据
china_data = areaTree[0]['children']
china_list = []
for a in range(len(china_data)):
    province = china_data[a]['name']
    province_list = china_data[a]['children']
    for b in range(len(province_list)):
        city = province_list[b]['name']
        total = province_list[b]['total']
        today = province_list[b]['today']
        china_dict = {'province': province, 'city': city, 'total': total, 'today': today}
        china_list.append(china_dict)

china_data = pd.DataFrame(china_list)
china_data.head()


# 定义数据处理函数
def confirm(x):
    return eval(str(x))['confirm']


def suspect(x):
    return eval(str(x))['suspect']


def dead(x):
    return eval(str(x))['dead']


def heal(x):
    return eval(str(x))['heal']


# 函数映射
china_data['confirm'] = china_data['total'].map(confirm)
china_data['suspect'] = china_data['total'].map(suspect)
china_data['dead'] = china_data['total'].map(dead)
china_data['heal'] = china_data['total'].map(heal)
china_data['addconfirm'] = china_data['today'].map(confirm)
china_data['addsuspect'] = china_data['today'].map(suspect)
china_data['adddead'] = china_data['today'].map(dead)
china_data['addheal'] = china_data['today'].map(heal)
china_data = china_data[
    ["province", "city", "confirm", "suspect", "dead", "heal", "addconfirm", "addsuspect", "adddead", "addheal"]]
china_data.head()

global_data = pd.DataFrame(data['areaTree'])
global_data['confirm'] = global_data['total'].map(confirm)
global_data['suspect'] = global_data['total'].map(suspect)
global_data['dead'] = global_data['total'].map(dead)
global_data['heal'] = global_data['total'].map(heal)
global_data['addconfirm'] = global_data['today'].map(confirm)
global_data['addsuspect'] = global_data['today'].map(suspect)
global_data['adddead'] = global_data['today'].map(dead)
global_data['addheal'] = global_data['today'].map(heal)
world_name = pd.read_excel("../others/世界各国中英文对照.xlsx")
global_data = pd.merge(global_data, world_name, left_on="name", right_on="中文", how="inner")
global_data = global_data[
    ["name", "英文", "confirm", "suspect", "dead", "heal", "addconfirm", "addsuspect", "adddead", "addheal"]]
global_data.head()

chinaDayList = pd.DataFrame(data['chinaDayList'])
chinaDayList = chinaDayList[['date', 'confirm', 'suspect', 'dead', 'heal']]
chinaDayList.head()

chinaDayAddList = pd.DataFrame(data['chinaDayAddList'])
chinaDayAddList = chinaDayAddList[['date', 'confirm', 'suspect', 'dead', 'heal']]
chinaDayAddList.head()

# from pyecharts.charts import *  # 导入所有图表
# from pyecharts import options as opts
# # 导入pyecharts的主题（如果不使用可以跳过）
# from pyecharts.globals import ThemeType

total_pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, width='500px', height='350px'))  # 设置主题，和画布大小
total_pie.add("", [list(z) for z in zip(chinaTotal.keys(), chinaTotal.values())],
              center=["50%", "50%"],  # 图的位置
              radius=[50, 80])  # 内外径大小
total_pie.set_global_opts(
    title_opts=opts.TitleOpts(title="全国总量", subtitle=("截止" + lastUpdateTime)))
total_pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{c}"))  # 标签格式
total_pie.render_notebook()

totaladd_pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, width='500px', height='350px'))  # 设置主题，和画布大小
totaladd_pie.add("", [list(z) for z in zip(chinaAdd.keys(), chinaAdd.values())],
                 center=["50%", "50%"],
                 radius=[50, 80])
totaladd_pie.set_global_opts(
    title_opts=opts.TitleOpts(title="昨日新增"))
totaladd_pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{c}"))  # 标签格式
totaladd_pie.render_notebook()

world_map = Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
world_map.add("", [list(z) for z in zip(list(global_data["英文"]), list(global_data["confirm"]))], "world",
              is_map_symbol_show=False)
world_map.set_global_opts(title_opts=opts.TitleOpts(title="2019_nCoV-世界疫情地图"),
                          visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                                                            pieces=[
                                                                {"min": 101, "label": '>100'},  # 不指定 max，表示 max 为无限大
                                                                {"min": 10, "max": 100, "label": '10-100'},
                                                                {"min": 0, "max": 9, "label": '0-9'}]))
world_map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
world_map.render_notebook()

# 数据处理
area_data = china_data.groupby("province")["confirm"].sum().reset_index()
area_data.columns = ["province", "confirm"]

area_map = Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
area_map.add("", [list(z) for z in zip(list(area_data["province"]), list(area_data["confirm"]))], "china",
             is_map_symbol_show=False)
area_map.set_global_opts(title_opts=opts.TitleOpts(title="2019_nCoV中国疫情地图"),
                         visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                                                           pieces=[
                                                               {"min": 1001, "label": '>1000', "color": "#893448"},
                                                               # 不指定 max，表示 max 为无限大
                                                               {"min": 500, "max": 1000, "label": '500-1000',
                                                                "color": "#ff585e"},
                                                               {"min": 101, "max": 499, "label": '101-499',
                                                                "color": "#fb8146"},
                                                               {"min": 10, "max": 100, "label": '10-100',
                                                                "color": "#ffb248"},
                                                               {"min": 0, "max": 9, "label": '0-9',
                                                                "color": "#fff2d1"}]))
area_map.render_notebook()

line1 = Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
line1.add_xaxis(list(chinaDayList["date"]))
line1.add_yaxis("治愈", list(chinaDayList["heal"]), is_smooth=True)
line1.add_yaxis("死亡", list(chinaDayList["dead"]), is_smooth=True)
line1.set_global_opts(title_opts=opts.TitleOpts(title="Line1-治愈与死亡趋势"))
line1.render_notebook()

line2 = Line(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
line2.add_xaxis(list(chinaDayList["date"]))
line2.add_yaxis("确诊", list(chinaDayList["confirm"]))
line2.add_yaxis("疑似", list(chinaDayList["suspect"]))
line2.set_global_opts(title_opts=opts.TitleOpts(title="Line2-确诊与疑似趋势"))
line2.render_notebook()

bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, width='900px', height='400px'))
bar.add_xaxis(list(chinaDayAddList["date"]))
bar.add_yaxis("确诊", list(chinaDayAddList["confirm"]))
bar.add_yaxis("疑似", list(chinaDayAddList["suspect"]))
bar.add_yaxis("死亡", list(chinaDayAddList["dead"]))
bar.add_yaxis("治愈", list(chinaDayAddList["heal"]))
bar.set_global_opts(title_opts=opts.TitleOpts(title="每日新增数据趋势"))
bar.render_notebook()

page = Page()
page.add(total_pie)
page.add(totaladd_pie)
page.add(world_map)
page.add(area_map)
page.add(line1)
page.add(line2)
page.add(bar)
page.render("./no_upload/2019_nCoV 可视化.html")
