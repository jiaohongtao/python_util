"""
https://blog.csdn.net/qq_42554007/article/details/108354167
"""
#  公众号：一行数据
from PIL import Image, ImageSequence

#  读取 GIF
im = Image.open("../images/daofang.gif")
#  GIF 图片流的迭代器
iterator = ImageSequence.Iterator(im)
index = 1
#  遍历图片流的每一帧
for frame in iterator:
    print("image %d: mode %s, size %s" % (index, frame.mode, frame.size))
    frame.save("../no_upload/daofang/img%d.png" % index)
    index += 1
#  把 GIF 拆分为图片流
imgs = [frame.copy() for frame in ImageSequence.Iterator(im)]
#  图片流反序
imgs.reverse()
#  将反序后的所有帧图像保存下来
imgs[0].save("reverse.gif", save_all=True, append_images=imgs[1:])
