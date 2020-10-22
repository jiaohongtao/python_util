import time  # 设置爬虫等待时间

import requests  # 获取网页数据
import xlwt
from bs4 import BeautifulSoup  # 解析网页数据

"""
href: https://www.jianshu.com/p/4292a8ba0192
"""


# 获取豆瓣网址并解析数据
def get_douban_books(url, num):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    res = requests.get(url, headers=headers)  # requests发起请求，静态网页用get
    soup = BeautifulSoup(res.text, 'html.parser')

    m = n = j = num

    items_title = soup.find_all("div", class_="pl2")
    for i in items_title:
        tag = i.find("a")
        # 去掉空格和换行符
        name = ''.join(tag.text.split())
        link = tag["href"]
        title_markdown = "[{}]\n({})".format(name, link)
        sheet.write(m, 0, title_markdown)
        sheet.col(0).width = 256 * len(title_markdown)
        m += 1

    items_author = soup.find_all("p", class_="pl")
    for i in items_author:
        author_markdown = i.text
        sheet.write(n, 1, author_markdown)
        sheet.col(1).width = len(author_markdown) * 256
        n += 1

    items_image = soup.find_all("a", class_="nbg")
    for i in items_image:
        tag = i.find("img")
        link = tag["src"]
        # image_markdown = "![]({})".format(link)
        # sheet.write(j, 2, image_markdown)
        sheet.write(j, 2, link)
        print(len(link))
        sheet.col(2).width = len(link) * 256
        j += 1


# 定义保存Excel的位置
workbook = xlwt.Workbook()  # 定义workbook
sheet = workbook.add_sheet('豆瓣读书')  # 添加sheet
head = ['书名', '作者', '图片']  # 表头
for h in range(len(head)):
    sheet.write(0, h, head[h])  # 把表头写到Excel里面去

# 豆瓣一共有10页数据
# 先形成网址 豆瓣是25个为一页
url = 'https://book.douban.com/top250?start={}'
urls = [url.format(num * 25) for num in range(10)]
page_num = [num * 25 + 1 for num in range(10)]
for i in range(10):
    get_douban_books(urls[i], page_num[i])
    print("第" + str(i + 1) + "页，完成")
    # 暂停 1 秒防止访问太快被封
    time.sleep(1)

# 保存 Excel 文件
workbook.save('../../no_upload/douban/book.xls')
