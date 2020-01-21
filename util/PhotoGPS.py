# 改进检测地区
import json
import os

import exifread
import requests


# ************************************************************************
# 代码功能：
#   1.读取所有图片文件的exif信息
#   2.提取图片中的经纬度，将度、分、秒转换为小数形式
#   3.利用百度地图API接口将经纬度转换成地址形式
# ************************************************************************


# 遍历文件夹及子文件夹中的所有图片,逐个文件读取exif信息
def get_pic_gps(pic_dir):
    items = os.listdir(pic_dir)
    for item in items:
        path = os.path.join(pic_dir, item)
        if os.path.isdir(path):
            get_pic_gps(path)
        else:
            image_read(path)


# 将经纬度转换为小数形式
def convert_to_decimal(*gps):
    # 度
    if '/' in gps[0]:
        deg = gps[0].split('/')
        if deg[0] == '0' or deg[1] == '0':
            gps_d = 0
        else:
            gps_d = float(deg[0]) / float(deg[1])
    else:
        gps_d = float(gps[0])
    # 分
    if '/' in gps[1]:
        minu = gps[1].split('/')
        if minu[0] == '0' or minu[1] == '0':
            gps_m = 0
        else:
            gps_m = (float(minu[0]) / float(minu[1])) / 60
    else:
        gps_m = float(gps[1]) / 60
    # 秒
    if '/' in gps[2]:
        sec = gps[2].split('/')
        if sec[0] == '0' or sec[1] == '0':
            gps_s = 0
        else:
            gps_s = (float(sec[0]) / float(sec[1])) / 3600
    else:
        gps_s = float(gps[2]) / 3600

    decimal_gps = gps_d + gps_m + gps_s
    # 如果是南半球或是西半球
    if gps[3] == 'W' or gps[3] == 'S' or gps[3] == "83" or gps[3] == "87":
        return str(decimal_gps * -1)
    else:
        return str(decimal_gps)


# 读取图片的经纬度和拍摄时间
def image_read(path):
    f = open(path, 'rb')
    GPS = {}
    Data = ""
    try:
        tags = exifread.process_file(f)
    except:
        return
    # print(tags)
    '''
    for tag in tags:               
        print(tag,":",tags[tag])
    '''

    # 南北半球标识
    if 'GPS GPSLatitudeRef' in tags:

        GPS['GPSLatitudeRef'] = str(tags['GPS GPSLatitudeRef'])
        # print(GPS['GPSLatitudeRef'])
    else:
        GPS['GPSLatitudeRef'] = 'N'  # 缺省设置为北半球

    # 东西半球标识
    if 'GPS GPSLongitudeRef' in tags:
        GPS['GPSLongitudeRef'] = str(tags['GPS GPSLongitudeRef'])
        # print(GPS['GPSLongitudeRef'])
    else:
        GPS['GPSLongitudeRef'] = 'E'  # 缺省设置为东半球

    # 海拔高度标识
    if 'GPS GPSAltitudeRef' in tags:
        GPS['GPSAltitudeRef'] = str(tags['GPS GPSAltitudeRef'])

    # 获取纬度
    if 'GPS GPSLatitude' in tags:
        lat = str(tags['GPS GPSLatitude'])
        # 处理无效值
        if lat == '[0, 0, 0]' or lat == '[0/0, 0/0, 0/0]':
            return

        deg, minu, sec = [x.replace(' ', '') for x in lat[1:-1].split(',')]
        # 将纬度转换为小数形式
        GPS['GPSLatitude'] = convert_to_decimal(deg, minu, sec, GPS['GPSLatitudeRef'])

    # 获取经度
    if 'GPS GPSLongitude' in tags:
        lng = str(tags['GPS GPSLongitude'])
        # print(lng)

        # 处理无效值
        if lng == '[0, 0, 0]' or lng == '[0/0, 0/0, 0/0]':
            return

        deg, minu, sec = [x.replace(' ', '') for x in lng[1:-1].split(',')]
        # 将经度转换为小数形式
        GPS['GPSLongitude'] = convert_to_decimal(deg, minu, sec, GPS['GPSLongitudeRef'])  # 对特殊的经纬度格式进行处理

    # 获取海拔高度
    if 'GPS GPSAltitude' in tags:
        GPS['GPSAltitude'] = str(tags["GPS GPSAltitude"])

    # 获取图片拍摄时间
    if 'Image DateTime' in tags:
        GPS["DateTime"] = str(tags["Image DateTime"])
        print(GPS["DateTime"])
    elif "EXIF DateTimeOriginal" in tags:
        GPS["DateTime"] = str(tags["EXIF DateTimeOriginal"])
        print(GPS["DateTime"])
    if 'Image Make' in tags:
        print('照相机制造商：', tags['Image Make'])
    if 'Image Model' in tags:
        print('照相机型号：', tags['Image Model'])
    if 'Image ExifImageWidth' in tags:
        print('照片尺寸：', tags['EXIF ExifImageWidth'], tags['EXIF ExifImageLength'])

    if 'GPSLatitude' in GPS:
        # 将经纬度转换为地址
        convert_gps_to_address(GPS)


# 利用百度全球逆地理编码服务（Geocoder）Web API接口服务将经纬转换为位置信息
def convert_gps_to_address(GPS):
    secret_key = 'zbLsuDDL4CS2U0M4KezOZZbGUY9iWtVf'  # 百度密钥
    lat, lng = GPS['GPSLatitude'], GPS['GPSLongitude']
    # 注意coordtype为wgs84ll(GPS经纬度),否则定位会出现偏差
    baidu_map_api = "http://api.map.baidu.com/geocoder/v2/?coordtype=wgs84ll&location={0},{1}&output=json&pois=0&ak={2}".format(
        lat, lng, secret_key)
    content = requests.get(baidu_map_api).text
    gps_address = json.loads(content)
    # 结构化的地址
    print(gps_address)
    formatted_address = gps_address["result"]["formatted_address"]
    # 国家（若需访问境外POI，需申请逆地理编码境外POI服务权限）
    country = gps_address["result"]["addressComponent"]["country"]
    # 省
    province = gps_address["result"]["addressComponent"]["province"]
    # 城市
    city = gps_address["result"]["addressComponent"]["city"]
    # 区
    district = gps_address["result"]["addressComponent"]["district"]
    # 语义化地址描述
    sematic_description = gps_address["result"]["sematic_description"]
    # 将转换后的信息写入文件
    with open("gps_address.csv", "a+") as csv:
        csv.write(GPS[
                      "DateTime"] + "|" + formatted_address + "|" + country + "|" + province + "|" + city + "|" + district + "|" + sematic_description + "\n")


if __name__ == "__main__":
    get_pic_gps("C:/Users/jiaohongtao/Desktop/imgs/PhotoGPS/second")
