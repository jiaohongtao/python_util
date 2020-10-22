import time  # 设置爬虫等待时间

import requests  # 获取网页数据
import xlwt
from bs4 import BeautifulSoup  # 解析网页数据

"""
获取豆瓣租房信息
获取excel后会产生空白行，后续优化
也可以根据该操作去除 https://jingyan.baidu.com/article/cbcede075ad25202f50b4d52.html
"""


# 获取豆瓣网址并解析数据
def get_douban_books(url, num):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    res = requests.get(url, headers=headers)  # requests发起请求，静态网页用get
    soup = BeautifulSoup(res.text, 'html.parser')

    m = n = num

    item_a_title = soup.find_all("td", class_="title")
    for item in item_a_title:
        tag_a = item.find("a")
        name = tag_a["title"]
        link = tag_a["href"]
        not_contains = ["八通线", "天通苑", "宋家庄", "龙泽", "后沙峪", "亦庄", "密云", "房山", "通州",
                        "石景山",
                        "2700", "2800", "2900", "3000", "3100", "3200", "3300", "3300", "3400"]
        # contains = ["牡丹园" "健德门", "西土城", "北土城", "安贞门", "惠新西街南口", "芍药居", "十号线",
        #             "10号线", "1分钟", "2分钟", "3分钟", "4分钟", "5分钟"]
        flag = False
        for nc in not_contains:
            if nc in name:
                flag = True
        if not flag:
            # print("[{}]({})".format(name, link))
            sheet.write(m, 0, name)
            # sheet.col(0).width = 512 * len(name)
            # sheet.col(0).width = 512 * 50
            sheet.write(n, 1, link)
            # sheet.col(1).width = 256 * len(link)
            with open("../../no_upload/douban.txt", "wb") as f:
                f.write(requests.get(i['hoverURL']).content)
            m += 1
            n += 1
        # for c in contains:
        #     if c in name:
        #         sheet.write(m, 0, name)
        #         sheet.col(0).width = 256 * len(name)
        #         sheet.write(n, 1, link)
        #         sheet.col(1).width = 256 * len(link)
        #         m += 1
        #         n += 1


# 定义保存Excel的位置
workbook = xlwt.Workbook()  # 定义workbook
sheet = workbook.add_sheet('豆瓣租房')  # 添加sheet
head = ['租房信息', '地址']  # 表头
for h in range(len(head)):
    sheet.write(0, h, head[h])  # 把表头写到Excel里面去
    sheet.col(0).width = 512 * 50
    sheet.col(1).width = 256 * 50

# 获取的页数
all_page = 5
# 每页个数
page_size = 30
url = 'https://www.douban.com/group/beijingzufang/discussion?start={}'
urls = [url.format(num * page_size) for num in range(all_page)]
page_num = [num * page_size + 1 for num in range(all_page)]
for i in range(all_page):
    get_douban_books(urls[i], page_num[i])
    print("==========第" + str(i + 1) + "页，完成==========")
    # 暂停 1 秒防止访问太快被封
    time.sleep(1)

# 保存 Excel 文件
workbook.save('../../no_upload/douban/douban_zufang.xls')
print("写入完成！")
