# coding = utf-8
# from bs4 import BeautifulSoup        # 用于解析网页源代码的模块
import base64
import json

import requests  # 用于获取网页内容的模块
from Crypto.Cipher import AES
from jsonpath import jsonpath

"""
我使用的第二种：https://www.cnblogs.com/bcaixl/p/13928629.html
"""


# 获取params 参数的函数
def get_params():
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def AES_encrypt(text, key, iv):
    text = text.encode('utf-8')
    pad = 16 - len(text) % 16
    text = text + (pad * chr(pad)).encode('utf-8')  # 需要转成二进制，且可以被16整除
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)  # .encode('utf-8')
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text.decode('utf-8')


def get_json(url, params, encSecKey):
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content


def handle_json():
    """通过request返回的json结果，对结果进行处理"""
    ressult_str = ressult_b.decode('utf-8')  # 结果转码为str类型
    json_text = json.loads(ressult_str)  # 加载为json格式
    L = []
    for i in range(len(jsonpath(json_text, '$..songs[*].id'))):  # 根据id获取列表条数
        D = {'num': 'null', 'name': 'null', 'id': 'null', 'singer': 'null', 'song_sheet': 'null'}  # 初始化字典
        D['num'] = i
        D['name'] = '/'.join(jsonpath(json_text, "$..songs[" + str(i) + "].name"))  # 获取名称
        D['id'] = str(jsonpath(json_text, "$..songs[" + str(i) + "].id")[0])  # 获取ID且获取第一个ID值并转化为str类型
        D['singer'] = '/'.join(jsonpath(json_text, "$..songs[" + str(i) + "].ar[*].name"))  # 获取歌手列表
        al_list = jsonpath(json_text, "$..songs[" + str(i) + "].al.name")  # 获取专辑列表
        al = '/'.join(al_list)  # 将获取的专辑列表合并
        D['song_sheet'] = "《" + al + "》"
        L.append(D)
    return L


def load_song(num, result):
    if isinstance(int(num), int):
        num = int(num)
        if num >= 0 and num <= len(result):
            song_id = ressult[num]['id']
            song_down_link = "http://music.163.com/song/media/outer/url?id=" + ressult[num][
                'id'] + ".mp3"  # 根据歌曲的 ID 号拼接出下载的链接。歌曲直链获取的方法参考文前的注释部分。
            print("歌曲正在下载...")
            response = requests.get(song_down_link, headers=headers).content  # 亲测必须要加 headers 信息，不然获取不了。
            f = open(ressult[num]['name'] + ".mp3", 'wb')  # 以二进制的形式写入文件中
            f.write(response)
            f.close()
            print("下载完成.\n\r")
        else:
            print("你输入的数字不在歌曲列表范围，请重新输入")

    else:
        print("请输入正确的歌曲序号")


if __name__ == "__main__":

    search_name = input("请输入你想要在网易云音乐中搜索的单曲：")
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
    }
    first_param = r'{"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":"' + search_name + r'","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}'
    second_param = "010001"
    third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    forth_param = "0CoJUm6Qyw8W8jud"
    url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
    params = get_params()
    encSeckey = get_encSecKey()
    ressult_b = get_json(url, params, encSeckey)
    ressult = handle_json()  # 过滤出需要的数据，存入到result中
    print("%3s %-35s %-20s %-20s " % ("序号", "  歌名", "歌手", "专辑"))
    for i in range(len(ressult)):
        print("%3s %-35s %-20s %-20s " % (
            ressult[i]["num"], ressult[i]["name"], ressult[i]["singer"], ressult[i]["song_sheet"]))
    num = input("请输入你想要下载歌曲的序号/please input the num you want to download：")
    load_song(num, ressult)  # 下载歌曲
