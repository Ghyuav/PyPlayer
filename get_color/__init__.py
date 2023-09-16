from PIL import Image

def RGB_to_Hex(rgb):
    RGB = rgb.split(',')            # 将RGB格式划分开来
    color = '#'
    for i in RGB:
        num = int(i)
        # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color

def get_dominant_colors(img):
    image = img
    
    # 缩小图片，否则计算机压力太大
    small_image = image.resize((80, 80))
    result = small_image.convert(
        "P", palette=Image.ADAPTIVE, colors=1
    )  
	
    palette = result.getpalette()
    color_counts = sorted(result.getcolors(), reverse=True)

    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index * 3 : palette_index * 3 + 3]

    return RGB_to_Hex(f'{dominant_color[0]},{dominant_color[1]},{dominant_color[2]}')
