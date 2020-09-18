#  -*-coding:utf-8-*-

import sys
import you_get

"""
下载哔哩哔哩视频
https://blog.csdn.net/minge89/article/details/108414176

下载单个：you-get https://www.bilibili.com/video/BV1NJ411J79W
下载所有：you-get https://www.bilibili.com/video/BV1NJ411J79W --playlist
指定目录：you-get -o E:/movie https://www.bilibili.com/video/BV1NJ411J79W
"""

def download(url, path):
    sys.argv = ['you-get', '-o', path, url]
    you_get.main()


if __name__ == '__main__':
    #  视频网站的地址
    # https://www.bilibili.com/bangumi/play/ep118488?from=search&seid=5050973611974373611
    # https://www.bilibili.com/video/BV1NJ411J79W
    url = 'https://www.bilibili.com/video/BV1NJ411J79W'
    #  视频输出的位置
    path = '../video/'
    # path = 'E:/Mixed/MadGod/'
    download(url, path)
