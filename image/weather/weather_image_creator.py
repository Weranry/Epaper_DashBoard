from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

class WeatherImageCreator:
    def __init__(self):
        font_path = os.path.join('assets', 'simhei.ttc')
        icon_font_path = os.path.join('assets', 'weather-icon.ttf')
        self.font = ImageFont.truetype(font_path, 18)
        self.icon_font = ImageFont.truetype(icon_font_path, 50)  # 图标字体

    def create_weather_image(self, weather_data):
        img = Image.new('P', (400, 300))
        img.putpalette([
            255, 255, 255,  # 白色
            0, 0, 0,        # 黑色
            255, 0, 0       # 红色
        ])
        draw = ImageDraw.Draw(img)

        # 天气图标映射
        icon_map = {
            '晴': '',
            '多云': '',
            '少云': '',
            '晴间多云': '',
            '阴': '',
            '阵雨': '',
            '强阵雨': '',
            '雷阵雨': '',
            '强雷阵雨': '',
            '雷阵雨伴有冰雹': '',
            '小雨': '',
            '中雨': '',
            '大雨': '',
            '极端降雨': '',
            '毛毛雨/细雨': '',
            '暴雨': '',
            '大暴雨': '',
            '特大暴雨': '',
            '冻雨': '',
            '小到中雨': '',
            '中到大雨': '',
            '大到暴雨': '',
            '暴雨到大暴雨': '',
            '大暴雨到特大暴雨': '',
            '小雪': '',
            '中雪': '',
            '大雪': '',
            '暴雪': '',
            '雨夹雪': '',
            '雨雪天气': '',
            '阵雨夹雪': '',
            '阵雪': '',
            '小到中雪':'',
            '中到大雪':'',
            '大到暴雪':'',
            '雪':'',
            '薄雾': '',
            '雾': '',
            '霾': '',
            '扬沙': '',
            '浮尘': '',
            '沙尘暴': '',
            '强沙尘暴': '',
            '浓雾': '',
            '强浓雾': '',
            '中度霾': '',
            '重度霾': '',
            '严重霾': '',
            '大雾': '',
            '特强浓雾': '',
            '热': '',
            '冷': '',
            '未知': ''
        }

        # 获取天气图标
        condition = weather_data.get('condition', '未知')
        icon = icon_map.get(condition, '')

        # 绘制天气图标
        draw.text((10, 10), icon, font=self.icon_font, fill=1)

        # 简单罗列天气信息
        y_position = 70
        for key, value in weather_data.items():
            draw.text((10, y_position), f"{key}: {value}", font=self.font, fill=1)
            y_position += 20

        img = img.convert('RGB')
        return img

    def get_image_bytes(self, img):
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=95, subsampling=0)
        img_io.seek(0)
        return img_io 