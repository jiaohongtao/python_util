import os
import time

import xlrd
import xlutils.copy
import xlwt

"""
python一键合并上千个Excel表
href: https://blog.csdn.net/qiukui111/article/details/107096970
公司老板需求：

    1. 将上千个Excel表合并成一个表里
    2. 不管你用什么方法，实现效果就行
"""
# #################################### 代码走起来呀！！！
"""
思路分析：
    1. 创建一个空表名叫"总表"，表格形式须和合并表的一样
    2. 获取需要合并文件夹中的所有excel表的名字（文件名)
    3. 开始遍历excel表
    4. 先读取数据，然后写入事先创建好总表中
    5. 当读取完下一个待合并表的数据，然后准备写入到总表时，必须先获取到总表的行数，不然之前的数据将会被覆盖掉。
    6. 遍历结束，保存总表的数据
"""
"""
项目运行：
    1. 将所有需要合并的表放到一个文件夹中，名叫excels
    2. autoMerge.py文件和excels文件夹同级
    3. 运行该.py文件，会在把合并表放到destDir夹中
"""


# 1.总表初始化(不友好，还需要自行写好表头列表，对非程序员不友好)
def initExcel(path, excelTitle, excel_sheet_Name):
    """
    :param path: 合并总表的路径
    :param excelTitle: 总表的表头
    :param excel_sheet_Name: 合并总表的sheet名称
    :return: 返回总表是否初始化成功
    """
    try:
        # 创建一个工作簿
        book = xlwt.Workbook(encoding="utf-8")
        # 创建表单
        sheet = book.add_sheet(excel_sheet_Name)
        # 写入表头
        for i in range(0, len(excelTitle)):
            sheet.write(0, i, excelTitle[i])
        book.save(path)
        return True
    except Exception as e:
        return False


# 1.1 总表初始化(用来解决上面的问题)
def initExcel2(destExcel_path, sourceExcel_path, total_sheet_name):
    """

    :param destExcel_path: 合并总表excel的路径
    :param sourceExcel_path: 需要合并excel的路径
    :param total_sheet_name: 合并总表后sheet的名字
    :return: 返回False or True
    """
    try:
        # 创建一个工作簿
        book = xlwt.Workbook(encoding="utf-8")
        # 创建表单,并给表单起个名字
        sheet = book.add_sheet(total_sheet_name)
        # 获取待需合并excel的所有文件
        excel_name_list = get_All_Excelname(sourceExcel_path)
        # 一个待合并execl的路径
        excel_path = sourceExcel_path + "/" + excel_name_list[0]
        # 获取excel的sheet
        excel_sheet = get_excel_sheet(excel_path)
        # 获取excel的表头数据
        excel_title_list = excel_sheet.row_values(0)
        # 写入表头
        for i in range(0, len(excel_title_list)):
            sheet.write(0, i, excel_title_list[i])
        book.save(destExcel_path)
        return True
    except Exception as e:
        return False


# 2.获取需要合并的所有的excel文件名
def get_All_Excelname(path):
    """

    :param path: 待合并excel文件的路径
    :return:
    """
    excelName_list = os.listdir(path)
    # print(excelName_list)
    return excelName_list


# 返回excel表的sheet对象
def get_excel_sheet(path):
    # 打开指定路径的excle表
    book = xlrd.open_workbook(path)
    # 获取excle中的表单
    sheet = book.sheet_by_index(0)
    # 返回sheet对象
    return sheet


# 返回总表的wtbook,sheet对象
def get_total_excel_sheet(path):
    """

    :param path: 存放总表的path
    :return:
    """
    book = xlrd.open_workbook(path, formatting_info=True)
    wtbook = xlutils.copy.copy(book)
    wtsheet = wtbook.get_sheet(0)
    return wtbook, wtsheet


# 4. 开始遍历(合并excel表)
def writeExcel(destExcel_path, source_path, excelName_list):
    """

    :param destExcel_path: 合并总表存放的路径
    :param source_path: 需要合并excel的路径
    :param excelName_list: 需要合并excel表的文件名称
    :return:
    """
    # 用来记录总表中的行数
    total_excel_row = 1
    # 获取总表的book,sheet
    total_book, total_sheet = get_total_excel_sheet(destExcel_path)
    for excelName in excelName_list:
        # 文件路径
        excelPath = source_path + excelName
        # 获取表的sheet对象
        sheet = get_excel_sheet(excelPath)
        # 获取行数
        n_rows = sheet.nrows
        # 开始遍历读取数据，并写入数据
        for row_index in range(1, n_rows):
            # 获取一行的数据，列表形式
            row_data_list = sheet.row_values(row_index)
            # 将数据写入到总表中
            for j in range(0, len(row_data_list)):
                total_sheet.write(total_excel_row, j, str(row_data_list[j]))
            # 每写一行，总表行数加1
            total_excel_row = total_excel_row + 1
    total_book.save(destExcel_path)
    print("数据合并已完成")
    print("合并后的数据共有%d条" % (total_excel_row - 1))


# 创建文件夹
def makeDir(path):
    """
    :param path: 传入需要创建文件夹的路径
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)


def main():
    # 待需合并的excel文件夹路径
    source_excel_path = "C:\\Users\\jiaohongtao\\Desktop\\excelDir\\"
    # 存放合并后的excel表文件夹路径
    dest_dir = "C:\\Users\\jiaohongtao\\Desktop\\destExcelDir"
    # 创建文件夹
    makeDir(dest_dir)
    # 合并excel表名
    total_excel_name = "总表.xls"
    # 合并表存放路径
    total_excel_path = dest_dir + "/" + total_excel_name
    # 合并总表中的sheet的名字
    total_excel_sheet_name = "汇总表"
    # 初始化表
    flag = initExcel2(total_excel_path, source_excel_path, total_excel_sheet_name)
    if flag:
        # excelName_list = get_All_Excelname("./excels")
        excelName_list = get_All_Excelname(source_excel_path)
        # 打印有多少个excel表
        print("总共有%d个excel表需要合并" % len(excelName_list))
        # 写数据
        writeExcel(total_excel_path, source_excel_path, excelName_list)
    else:
        print("初始化表失败")


if __name__ == '__main__':
    main()
    time.sleep(3)
