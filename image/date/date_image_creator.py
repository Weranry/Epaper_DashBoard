from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from functions.date.date_calculator import DateCalculator  # 只导入 DateCalculator

class DateImageCreator:
    def __init__(self):
        font_path = os.path.join('assets', 'simhei.ttc')
        self.title_font = ImageFont.truetype(font_path, 18)
        self.content_font = ImageFont.truetype(font_path, 18)
        self.large_font = ImageFont.truetype(font_path, 120)

    def create_date_image(self, date_data):
        # 创建一个400x300的索引颜色图片，使用黑、白、红三色调色板
        img = Image.new('P', (400, 300))
        img.putpalette([
            255, 255, 255,  # 白色
            0, 0, 0,        # 黑色
            255, 0, 0       # 红色
        ])
        draw = ImageDraw.Draw(img)
        
        # 绘制公历日期和星期
        solar_text = f"{date_data['solar']['solar_year']}/{date_data['solar']['solar_month']}/{date_data['solar']['solar_day']} {date_data['solar']['weekday']}"
        draw.text((10, 10), solar_text, font=self.title_font, fill=1)

        # 绘制农历日期
        lunar_text = f"农历{date_data['lunar']['lunar_month']}{date_data['lunar']['lunar_day']}"
        draw.text((10, 38), lunar_text, font=self.title_font, fill=1)
        
        # 绘制干支纪年
        ganzhi_text = f"{date_data['ganzhi']['ganzhi_year']}[{date_data['ganzhi']['shengxiao']}年]"
        draw.text((10, 58), ganzhi_text, font=self.content_font, fill=1)
        ganzhi_text2 = f"{date_data['ganzhi']['ganzhi_month']} {date_data['ganzhi']['ganzhi_day']}"
        draw.text((10, 78), ganzhi_text2, font=self.content_font, fill=1)

        # 绘制放大版阳历日
        solar_day = date_data['solar']['solar_day']
        solar_day_bbox = draw.textbbox((0, 0), solar_day, font=self.large_font)
        draw.text(((400 - solar_day_bbox[2]) / 2, 100), solar_day, font=self.large_font, fill=1)
        
        # 绘制数九或伏
        if date_data['season']['fujiu']:
            draw.text((380, 10), date_data['season']['fujiu'], font=self.title_font, fill=1, anchor="ra")
        
        # 绘制物候和节气
        season_text = f"{date_data['season']['wu_hou']} {date_data['season']['hou']}"
        season_bbox = draw.textbbox((0, 0), season_text, font=self.content_font)
        draw.text(((400 - season_bbox[2]) / 2, 230), season_text, font=self.content_font, fill=1)
        
        # 绘制节日信息
        festival_text = f"{date_data['festival']['solar_festival']} {date_data['festival']['lunar_festival']}"
        festival_bbox = draw.textbbox((0, 0), festival_text, font=self.content_font)
        draw.text(((400 - festival_bbox[2]) / 2, 260), festival_text, font=self.content_font, fill=2)
        
        # 转换为24位RGB图像
        img = img.convert('RGB')
        return img

    def get_image_bytes(self, img):
        img_io = BytesIO()
        # 保存为JPEG，使用最高质量
        img.save(img_io, 'JPEG', quality=95, subsampling=0)  # 4:4:4 subsampling
        img_io.seek(0)
        return img_io 
