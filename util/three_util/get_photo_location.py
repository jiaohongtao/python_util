import json

import phone

"""
运用到的知识点：
截取字符串，数组转json字符串，读取文件内容，字符串长度，字符串以xx开头
"""


# 查询手机号全部信息 如：{'phone': '15900xxxxxx', 'province': '上海', 'city': '上海',
# 'zip_code': '200000', 'area_code': '021', 'phone_type': '移动'}
def find_phone_info(mobile):
    result = phone.Phone().find(mobile)
    # del result["zip_code"]
    # del result["area_code"]
    return result


# 读取文件，生成数据
def get_file_generate():
    list = []
    file = open('../files/phone_all.txt', encoding='UTF-8')
    line = file.readline()
    while line:
        # print(line, end="")
        if "TEL;CELL:" in line:
            # print(line, "")
            phone_num = line[9:].strip()
            if phone_num.startswith("+"):
                phone_num = phone_num[3:]
            if len(phone_num) == 11 and phone_num.startswith("1"):
                # {'phone': '18601067587', 'province': '北京', 'city': '北京',
                # 'zip_code': '100000', 'area_code': '010', 'phone_type': '联通'}
                # print(phone_num)
                info = find_phone_info(phone_num)
                # print("python 自带的手机号码查询方法（phone）：")
                obj = {}
                # obj["province"] = info["province"] + "-" + info["province"]
                obj["province"] = info["province"]
                obj["city"] = info["city"]
                obj["phone"] = info["phone"]
                obj["phone_type"] = info["phone_type"]
                list.append(obj)
                # print(info)

        line = file.readline()
    # print(list)
    # print(json.dumps(list, ensure_ascii=False))
    file.close()
    return list


if __name__ == "__main__":
    # phoneNum = '18332120276'
    # info = find_phone_info(phoneNum)
    # print("python 自带的手机号码查询方法（phone）：")
    # print(info)
    phone_list = get_file_generate()
    print(json.dumps(phone_list, ensure_ascii=False))

    dic = {}
    for item in phone_list:
        # 统计地区
        # {"河北-邢台":16,"河北-石家庄":126,"天津-天津":4,"河北-衡水":4,"河北-保定":5,"山西-太原":3,
        # "甘肃-兰州":1,"河北-张家口":2,"河北-承德":3,"新疆-乌鲁木齐":2,"河北-邯郸":1,"北京-北京":5,
        # "河北-沧州":1,"陕西-西安":1,"河北-唐山":1}
        # if item["location"] in dic.keys():
        #     dic[item["location"]] += 1
        # else:
        #     dic[item["location"]] = 1

        # # 统计运营商 {"移动": 123, "联通": 32, "电信": 20}
        # if item["phone_type"] in dic.keys():
        #     dic[item["phone_type"]] += 1
        # else:
        #     dic[item["phone_type"]] = 1

        # 省 {"河北": 159, "天津": 4, "山西": 3, "甘肃": 1, "新疆": 2, "北京": 5, "陕西": 1}
        if item["province"] in dic.keys():
            dic[item["province"]] += 1
        else:
            dic[item["province"]] = 1
    print(json.dumps(dic, ensure_ascii=False))
