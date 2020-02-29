from PIL import Image, ImageDraw, ImageFont

"""
源地址：https://blog.csdn.net/lantian_123/article/details/103900552
"""
content = '小年快乐'

# 图片尺寸
width, height = 553, 369
# 字体样式
font_type = 'C://Windows/Fonts/simsun.ttc'
# 字体大小
font = ImageFont.truetype(font_type, 50)

# 生成100张不同款式的小年海报
for i in range(100):
    # red = 100 + i
    red = i
    image = Image.new("RGBA", (width, height), color=f"rgb({red},39,37)")
    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(content, font=font)
    draw.text(((width - w) / 2, (height - h) / 2),
              content,
              fill="rgb(245,207,142)",
              spacing=18,
              font=font)
    # 生成图片
    file_name = f"{red + 1}.png"
    image.save("./no_upload/" + file_name, 'png')
    print(f"成功生成第{i + 1}张图片")
