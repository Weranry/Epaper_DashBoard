from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

class huangliImageACreator:
    def __init__(self):
        font_path = os.path.join('assets', 'simhei.ttf')
        # 进一步增大的大字体，用于显示农历日期、宜、忌
        self.large_font = ImageFont.truetype(font_path, 32)
        # 之前的小字体，用于显示干支日期、阳历日期、宜忌内容
        self.small_font = ImageFont.truetype(font_path, 16)

    def wrap_text(self, text, font, max_width, max_lines=2):
        """
        该函数用于将长文本按指定最大宽度进行换行处理，且最大行数不超过指定值
        :param text: 要处理的文本
        :param font: 使用的字体
        :param max_width: 最大宽度
        :param max_lines: 最大行数
        :return: 换行后的文本列表
        """
        lines = []
        if font.getlength(text) <= max_width:
            lines.append(text)
        else:
            words = text.split(' ')
            current_line = words[0]
            for word in words[1:]:
                if font.getlength(current_line + ' ' + word) <= max_width and len(lines) < max_lines:
                    current_line += ' ' + word
                else:
                    if len(lines) < max_lines:
                        lines.append(current_line)
                        current_line = word
                    else:
                        break
            if len(lines) < max_lines:
                lines.append(current_line)
        return lines

    def create_huangli_A_image(self, date_data):
        # 创建一个400x300的索引颜色图像，调色板包含白色、黑色和红色
        img = Image.new('P', (400, 300))
        img.putpalette([
            255, 255, 255,  # White
            0, 0, 0,        # Black
            255, 0, 0       # Red
        ])
        draw = ImageDraw.Draw(img)

        # 绘制农历日期，大字体
        lunar_date = date_data['lunar']
        lunar_text = f"农历{lunar_date['lunar_month']}{lunar_date['lunar_day']}"
        draw.text((10, 10), lunar_text, font=self.large_font, fill=1)

        # 绘制干支日期和属相，小字体
        ganzhi_date = date_data['ganzhi']
        ganzhi_text = f"{ganzhi_date['ganzhi_year']} {ganzhi_date['ganzhi_month']}{ganzhi_date['ganzhi_day']} [{ganzhi_date['shengxiao']}]"
        draw.text((10, 45), ganzhi_text, font=self.small_font, fill=1)

        # 绘制阳历日期和星期几，小字体
        solar_date = date_data['solar']
        solar_text = f"{solar_date['solar_year']}年{solar_date['solar_month']}月{solar_date['solar_day']}日 {solar_date['weekday']} {solar_date['xingzuo']}"
        draw.text((10, 75), solar_text, font=self.small_font, fill=1)

        # 绘制分割线
        draw.line((10, 105, 390, 105), fill=1)

        # 绘制宜，大字体
        draw.text((10, 115), "宜", font=self.large_font, fill=1)
        yiji = date_data['yiji']
        # 将逗号替换为空格
        yi_text = ' '.join(yiji['Yi'])
        # 处理宜的内容换行，最大两行
        yi_lines = self.wrap_text(yi_text, self.small_font, 380)
        for i, line in enumerate(yi_lines):
            draw.text((10, 150 + i * 20), line, font=self.small_font, fill=1)

        # 绘制忌，大字体
        draw.text((10, 195), "忌", font=self.large_font, fill=1)
        # 将逗号替换为空格
        ji_text = ' '.join(yiji['Ji'])
        # 处理忌的内容换行，最大两行
        ji_lines = self.wrap_text(ji_text, self.small_font, 380)
        for i, line in enumerate(ji_lines):
            draw.text((10, 230 + i * 20), line, font=self.small_font, fill=1)

        # 转换为RGB模式
        img = img.convert('RGB')
        return img

    def get_image_bytes(self, img):
        img_io = BytesIO()
        # 保存为JPEG格式，最高质量和4:4:4子采样
        img.save(img_io, 'JPEG', quality=95, subsampling=0)
        img_io.seek(0)
        return img_io