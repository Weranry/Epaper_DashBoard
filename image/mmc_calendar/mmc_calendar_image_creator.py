from PIL import Image
import os

def create_mmc_calendar_image(image_data):
    h, w = (640, 480)
    screen = image_data[16 + 480:-16]
    view = [0] * (640 * 480 // 8)

    for i in range(h // 8):
        for j in range(w):
            v = screen[i * w + j]
            view[j * h // 8 + i] = v ^ 0xff

    # 创建图像
    im = Image.frombytes('1', (h, w), bytes(view))
    im2 = im.transpose(method=Image.TRANSPOSE)

    # 创建一个新的空白图像，大小为800x480
    new_im = Image.new('1', (w, 800), 1)  # 1表示白色背景
    new_im.paste(im2, (0, 80))  # 将原图粘贴到新图的中间位置

    return new_im 