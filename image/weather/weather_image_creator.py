from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

class WeatherImageCreator:
    def __init__(self):
        self.font_path = os.path.join('assets', 'simhei.ttc')
        icon_font_path = os.path.join('assets', 'weather-icon.ttf')
        self.font = ImageFont.truetype(self.font_path, 18)
        self.icon_font = ImageFont.truetype(icon_font_path, 80)
        self.small_font = ImageFont.truetype(self.font_path, 14)

    def create_weather_image(self, weather_data):
        img = Image.new('P', (400, 300))
        img.putpalette([255,255,255, 0,0,0, 255,0,0])
        draw = ImageDraw.Draw(img)

        # 卡片背景
        card_width = 380
        draw.rectangle([(10,10), (card_width,90)], fill=0)
        draw.rectangle([(10,100), (card_width,290)], fill=0)

        # 天气图标映射
        icon_map = {
            '晴': '', '多云': '', '少云': '', '晴间多云': '', '阴': '',
            '阵雨': '', '强阵雨': '', '雷阵雨': '', '强雷阵雨': '',
            '雷阵雨伴有冰雹': '', '小雨': '', '中雨': '', '大雨': '',
            '极端降雨': '', '毛毛雨/细雨': '', '暴雨': '', '大暴雨': '',
            '特大暴雨': '', '冻雨': '', '小到中雨': '', '中到大雨': '',
            '大到暴雨': '', '暴雨到大暴雨': '', '大暴雨到特大暴雨': '',
            '小雪': '', '中雪': '', '大雪': '', '暴雪': '', '雨夹雪': '',
            '雨雪天气': '', '阵雨夹雪': '', '阵雪': '', '小到中雪':'',
            '中到大雪':'', '大到暴雪':'', '雪':'', '薄雾': '', '雾': '',
            '霾': '', '扬沙': '', '浮尘': '', '沙尘暴': '', '强沙尘暴': '',
            '浓雾': '', '强浓雾': '', '中度霾': '', '重度霾': '', '严重霾': '',
            '大雾': '', '特强浓雾': '', '热': '', '冷': '', '未知': ''
        }

        # 天气图标
        condition = weather_data['condition']
        draw.text((20, 15), icon_map[condition], font=self.icon_font, fill=1)

        # 更新时间
        time_font = ImageFont.truetype(self.font_path, 12)
        time_text = f"更新时间:{weather_data['current_time']}"
        draw.text((400 - time_font.getlength(time_text) - 10, 10), 
                time_text, font=time_font, fill=1)

        # 温度与天气名称
        condition_font = ImageFont.truetype(self.font_path, 24)
        temp_text = f"({weather_data['temperature']})"
        start_x, start_y = 120, 80 - condition_font.size - 5
        
        draw.text((start_x, start_y), condition, font=condition_font, fill=1)
        draw.text((start_x + condition_font.getlength(condition), start_y),
                temp_text, font=condition_font, fill=1)

        # 核心参数
        params = [
            ("风速", weather_data['wind']),
            ("湿度", weather_data['humidity']),
            ("体感", weather_data['feels_like']),
            ("紫外线", weather_data['uv']),
            ("气压", weather_data['pressure']),
            ("能见度", weather_data['visibility'])
        ]
        
        y_pos = 120
        for i in range(0, len(params), 2):
            x_offset = 40
            for label, value in params[i:i+2]:
                draw.text((x_offset, y_pos), f"{label}:{value}", font=self.font, fill=1)
                x_offset += 180
            y_pos += 40

        # 摘要信息
        abstract = weather_data['abstract']
        lines, current_line = [], []
        
        for char in abstract:
            if self.small_font.getlength(''.join(current_line + [char])) <= 360:
                current_line.append(char)
            else:
                lines.append(''.join(current_line))
                current_line = [char]
        lines.append(''.join(current_line))
        
        y_abstract = 290 - len(lines)*20
        for line in lines:
            line_width = self.small_font.getlength(line)
            draw.text(((400 - line_width)//2, y_abstract), line, font=self.small_font, fill=1)
            y_abstract += 20

        # 分割线
        draw.line([(10,100), (card_width,100)], fill=1, width=2)
        return img.convert('RGB')

    def get_image_bytes(self, img):
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=100, subsampling=0)
        img_io.seek(0)
        return img_io