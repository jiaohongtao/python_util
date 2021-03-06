# -*- coding: utf-8 -*-
import json
import re
import time

import requests

url = 'https://3g.dxy.cn/newh5/view/pneumonia'

headers = {
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding

total = re.search(r'window\.getStatisticsService = ({.*?})', response.text).group(1)
total = total + "]}"
print(total)
total = json.loads(total)

# 使用time
createTime = time.localtime(float(total['createTime'] / 1000))
modifyTime = time.localtime(float(total['modifyTime'] / 1000))
ruleCreateTime = time.strftime("%Y-%m-%d %H:%M:%S", createTime)
ruleModifyTime = time.strftime("%Y-%m-%d %H:%M:%S", modifyTime)
# print(ruleCreateTime)
print(ruleModifyTime)

data = {'全国': {}}

# data['全国'] = {}
data['全国']['累计确诊'] = total['confirmedCount']
data['全国']['现存确诊'] = total['currentConfirmedCount']
data['全国']['疑似'] = total['suspectedCount']
data['全国']['死亡'] = total['deadCount']
data['全国']['重症'] = total['seriousCount']
data['全国']['治愈'] = total['curedCount']

data['全国']['累计确诊新增'] = total['confirmedIncr']
data['全国']['现存确诊减少'] = total['currentConfirmedIncr']
data['全国']['境外输入'] = total['suspectedCount']
data['全国']['境外输入新增'] = total['suspectedIncr']
data['全国']['现存重症减少'] = total['seriousIncr']

cities = re.findall(r'{"provinceName":.*?]}', response.text)

for city in cities:
    city = json.loads(city)
    provinceShortName = city['provinceShortName']
    currentConfirmedCount = city['currentConfirmedCount']
    confirmedCount = city['confirmedCount']
    deadCount = city['deadCount']
    curedCount = city['curedCount']

    data[provinceShortName] = {}
    data[provinceShortName]['现存确诊'] = currentConfirmedCount
    data[provinceShortName]['确诊'] = confirmedCount
    data[provinceShortName]['死亡'] = deadCount
    data[provinceShortName]['治愈'] = curedCount

# for key in data:
#     print("%s : %s" % (key, data[key]))

with open("update.txt", "w+", encoding="utf-8") as f:
    f.write(ruleModifyTime + "\n")
    f.write("---------------------\n")
    for key in data:
        # print("%s : %s" % (key, data[key]))
        f.write("%s : %s" % (key, data[key]) + "\n")
    f.write("\n" + url)
