"""
https://blog.csdn.net/weixin_41308573/article/details/87021667
"""

import requests
from urllib import request
from lxml import etree
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'Host': 'music.163.com',
    'Referer': 'https://music.163.com/'
}


def selenium_get_html(url):
    """通过selenium获得页面源码"""
    # 无界面启动chrome
    options = webdriver.ChromeOptions()
    options.add_argument(
        'User-Agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"')
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    # 歌曲信息在frame框架内，进入frame框架得到源码
    driver.switch_to.frame('contentFrame')
    return driver.page_source


# 提取歌曲名称，演唱者姓名，和歌曲id以供选择
def search_input_song(url):
    """获取歌曲名字和id"""
    html = selenium_get_html(url)

    root = etree.HTML(html)
    id = root.xpath('//div[@class="srchsongst"]//div[@class="td w0"]//div[@class="text"]/a[1]/@href')
    artist = root.xpath('//div[@class="srchsongst"]//div[@class="td w1"]//div[@class="text"]/a[1]/text()')
    name = root.xpath('//div[@class="srchsongst"]//div[@class="td w0"]//div[@class="text"]//b/@title')

    id = [i.strip('/song?id==') for i in id]
    return zip(name, artist, id)


# 歌手默认选择第一位，所以仅得到第一位歌手的id
def search_input_artist(url):
    """获取歌手id"""
    html = selenium_get_html(url)

    root = etree.HTML(html)
    id = root.xpath('//div[@class="u-cover u-cover-5"]/a[1]/@href')

    return id[0].strip('/artist?id==')


# 提取歌单名称，和歌单id以供选择
def search_input_playlist(url):
    """获取歌单名字和id"""
    html = selenium_get_html(url)

    root = etree.HTML(html)
    id = root.xpath('//div[@class="u-cover u-cover-3"]/a/@href')
    name = root.xpath('//div[@class="u-cover u-cover-3"]//span/@title')

    id = [i.strip('/playlist?id==') for i in id]
    return zip(name, id)


# url为歌单或歌手的地址
def get_url(url):
    """从歌单中获取歌曲链接"""
    req = requests.get(url, headers=headers)

    root = etree.HTML(req.text)
    items = root.xpath('//ul[@class="f-hide"]//a')
    print(items)

    return items


# song_id为歌曲id, song_name为歌曲名称
def download_song(song_id, song_name, path):
    """通过外链下载歌曲"""

    url = 'https://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)

    # get请求设置禁止网页跳转，即allow_redirects=False
    req = requests.get(url, headers=headers, allow_redirects=False)
    song_url = req.headers['Location']
    try:
        # path在主函数中输入
        request.urlretrieve(song_url, path + "/" + song_name + ".mp3")
        print("{}--下载完成".format(song_name))
    except:
        print("{}--下载失败".format(song_name))


# download_song(1380720351, "1380720351", "./")
download_song(1380720351, "悠哉山歌大王", "./")
