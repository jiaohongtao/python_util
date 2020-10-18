import os

"""
https://blog.csdn.net/zhong871004/article/details/81214567
path--文件路径
old--要替换的字符串
new--替换后的字符串
"""


def batch_file_rename(path, old, new):
    global oldDir, file
    files = os.listdir(path)
    for file in files:
        oldDir = os.path.join(path, file)  # 原来的文件路径
        if os.path.isdir(oldDir):
            continue
        newName = file.replace(old, new)  # 新文件名
        newDir = os.path.join(path, newName)  # 新文件路径
        os.rename(oldDir, newDir)  # 重命名


# 替换文件夹
# def bunchDirRename(path, old, new):
#     dirs = os.listdir(path)
#     for dir in dirs:
#         oldDir = os.path.join(path, dir)
#         if os.path.isfile(oldDir):
#             continue
#         newName = dir.replace(old, new)
#         newDir = os.path.join(path, newName)
#         os.rename(oldDir, newDir)  # 重命名


batch_file_rename("../no_upload/qianzhui_wenjian/", "ha", "")
