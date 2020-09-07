# -*-coding:GBK-*-
# 1.导入所需模块
import requests
import os

# 创建lol文件夹
os.mkdir("lol")

# 2.读取js文件，获取英雄id（hero_id）
url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
response = requests.get(url, headers=headers)
json_list = response.json()
hero_list = json_list['hero']
print("英雄总数：", len(hero_list))

try:
    # 3.根据hero_id拼接URL获取该英雄皮肤地址
    for m in range(len(hero_list)):
        # 英雄编号
        hero_id = hero_list[m]['heroId']
        print(hero_id)
        # 英雄名称
        hero_name = hero_list[m]['name']
        print(hero_name)
        url2 = 'http://game.gtimg.cn/images/lol/act/img/js/hero/' + hero_id + '.js'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        response2 = requests.get(url2, headers=headers)
        json_list2 = response2.json()
        img_list = json_list2['skins']
        print(hero_name + "皮肤数量：", len(img_list))
        # 遍历皮肤地址下载图片
        for n in range(len(img_list)):
            imgPath = img_list[n]['mainImg']
            if imgPath == "":
                continue
            skin_name = img_list[n]['name'].replace("/", " ")
            picture = requests.get(imgPath).content
            # 打印图片网址
            print(imgPath)
            # 下载图片 文件路径为: lol/英雄名-皮肤名.jpg
            with open('lol/' + hero_name + ' - ' + skin_name + '.jpg', 'wb') as f:
                f.write(picture)

except KeyError as e:
    print('程序执行完毕!')
