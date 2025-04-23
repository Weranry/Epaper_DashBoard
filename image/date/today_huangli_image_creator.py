from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
# 此行为预留行，后续可添加新的导入语句或其他代码
import os

class huangliImageCreator:
    def __init__(self):
        # 构建字体文件路径，字体文件存于 assets 目录下的 simhei.ttc
        font_path = os.path.join('assets', 'simhei.ttf')
        # 创建字号为 16 的字体对象
        self.font = ImageFont.truetype(font_path, 16)
        # 创建字号为 14 的字体对象
        self.small_font = ImageFont.truetype(font_path, 14)

    # 修正缩进，让函数体正确缩进
    def create_huangli_image(self, date_data):
        # 创建一个 400x300 的索引颜色图像，调色板包含白色、黑色和红色
        img = Image.new('P', (400, 300))
        # 设置调色板，分别为白色、黑色和红色
        img.putpalette([
            255, 255, 255,  # 白色
            0, 0, 0,        # 黑色
            255, 0, 0       # 红色
        ])
        # 创建一个可在图像上绘图的对象
        draw = ImageDraw.Draw(img)

        # 绘制水平分割线，将图像分为四个主要部分
        draw.line([(0, 80), (400, 80)], fill=1, width=1)
        draw.line([(0, 160), (400, 160)], fill=1, width=1)
        draw.line([(0, 240), (400, 240)], fill=1, width=1)

        # 顶部区域：绘制垂直线，将顶部区域均分为五部分
        for x in range(80, 400, 80):
            draw.line([(x, 0), (x, 80)], fill=1, width=1)

        # 中间两个区域：绘制垂直线，将中间区域均分为四部分
        for x in range(100, 400, 100):
            draw.line([(x, 80), (x, 160)], fill=1, width=1)

        # 在顶部区域绘制吉神信息
        jishen = date_data['jishen']
        for i, (key, value) in enumerate(jishen.items()):
            # 计算文本绘制的 x 坐标
            x = i * 80 + 40
            # 绘制吉神名称
            draw.text((x, 20), key, fill=1, font=self.font, anchor='mm')
            # 绘制吉神对应的值
            draw.text((x, 60), value, fill=1, font=self.font, anchor='mm')

        # 在中间第一个区域绘制其他参数信息
        middle_items = [
            ('太岁', date_data['ganzhi']),
            ('胎神', date_data['taishen']),
            ('冲煞', date_data['chongsha']),
            ('二十八宿', date_data['ershibaxingxiu'])
        ]

        for i, (key, value) in enumerate(middle_items):
            # 计算文本绘制的 x 坐标
            x = i * 100 + 50
            # 在第一个中间区域绘制参数名称
            draw.text((x, 100), key, fill=1, font=self.font, anchor='mm')
            # 在第一个中间区域绘制参数值
            draw.text((x, 140), value, fill=1, font=self.font, anchor='mm')

        # 中间第二个区域留空，后续可扩展内容

        # 在底部区域绘制彭祖百忌信息
        draw.text((200, 260), "彭祖百忌", fill=1, font=self.font, anchor='mm')
        draw.text((200, 290), date_data['pengzubaiji'], fill=1, font=self.font, anchor='mm')

        # 将图像转换为 RGB 模式
        img = img.convert('RGB')
        return img

    def get_image_bytes(self, img):
        # 创建一个内存中的字节流对象
        img_io = BytesIO()
        # 将图像以 JPEG 格式保存到字节流中，采用最高质量和 4:4:4 子采样
        img.save(img_io, 'JPEG', quality=95, subsampling=0)
        # 将文件指针移动到字节流的起始位置
        img_io.seek(0)
        return img_io