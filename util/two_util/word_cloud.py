"""
WordCloud生成卡卡西忍术词云
https://blog.csdn.net/ZackSock/article/details/103517841
"""

import imageio
import jieba
import wordcloud

# 1、准备文本
f = open('../files/lufei.txt', encoding='utf-8')
kkx = f.read()
kkx = jieba.cut(kkx)
kkx = " ".join(kkx)

# 2、生成图片的nd-array，传入图片路径
im = imageio.imread('../images/lufei_first.jpg')

# 3、获取一个图形颜色生成器
image_color = wordcloud.ImageColorGenerator(im)

# 4、创建词云对象
wc = wordcloud.WordCloud(
    # 设置宽为600
    width=600,
    # 设置高为800
    height=800,
    # 设置背景颜色
    background_color='white',
    # 设置字体，如果文本数据是中文一定要设置，不然就是方块
    font_path='msyh.ttc',
    # 设置图片的形状
    mask=im,
    # 设置轮廓粗细
    contour_width=1,
    # # 设置轮廓颜色
    contour_color='pink'
)

# 5、根据文本生成词云
wc.generate(kkx)

# 根据图片颜色重绘
rwc = wc.recolor(color_func=image_color)
rwc.to_file('../no_upload/lufei.png')
