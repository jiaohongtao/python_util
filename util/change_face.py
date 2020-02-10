import base64

import requests


# faceplus++获取
key = 'key'
secret = '密钥'


# 获取图片的人脸特征参数
def find_face(imgpath):
    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {'api_key': key, 'api_secret': secret, 'image_url': imgpath, 'return_landmark': 1}
    files = {'image_file': open(imgpath, 'rb')}
    response = requests.post(url, data=data, files=files)
    res_json = response.json()
    faces = res_json['faces'][0][
        'face_rectangle']  # 获取面部大小的四个值，分别为长宽高低{'width': 176, 'top': 128, 'left': 80, 'height': 176}
    return faces


# 换脸,函数传参中number表示两张脸的相似度为99%
def change_face(image_1, image_2, number=99):
    url = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"
    find_p1 = find_face(image_1)
    find_p2 = find_face(image_2)
    rectangle1 = str(str(find_p1['top']) + ',' + str(find_p1['left']) + ',' + str(find_p1['width']) + ',' + str(
        find_p1['height']))  # 得到一个坐标
    rectangle2 = str(
        str(find_p2['top']) + ',' + str(find_p2['left']) + ',' + str(find_p2['width']) + ',' + str(find_p2['height']))

    page1 = open(image_1, 'rb')  # 以二进制打开图片1
    page1_64 = base64.b64encode(page1.read())  # 将字符串转成成base64编码
    page1.close()

    page2 = open(image_2, 'rb')
    page2_64 = base64.b64encode(page2.read())
    page2.close()

    data = {'api_key': key, 'api_secret': secret, 'template_base64': page1_64,
            'template_rectangle': rectangle1, 'merge_base64': page2_64, 'merge_rectangele': rectangle2,
            'merge_rate': number}
    response = requests.post(url, data=data).json()
    results = response['result']
    image = base64.b64decode(results)
    with open('./images/dist.jpg', 'wb') as file:
        file.write(image)
    print(response)


if __name__ == '__main__':
    change_face('./images/aa.jpg', './images/dd.jpg')
