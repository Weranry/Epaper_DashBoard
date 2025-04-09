from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os


class SteamImageCreator:
    def __init__(self):
        font_path = os.path.join('assets','simhei.ttc')
        self.title_font = ImageFont.truetype(font_path, 18)
        self.content_font = ImageFont.truetype(font_path, 18)

    def create_steam_image(self, steam_data):
        # 创建一个索引颜色图片，调色板为白、黑、红
        img = Image.new('P', (400, 300))
        img.putpalette([
            255, 255, 255,  # 白色
             0, 0, 0,        # 黑色
            255, 0, 0       # 红色
        ])
        draw = ImageDraw.Draw(img)
                # Top line: Steam | Username
        draw.text((10, 10), "Steam | ", font=self.title_font, fill=1)
        steam_text_width = draw.textlength("Steam | ", font=self.title_font)
        draw.text((10 + steam_text_width, 10), steam_data['nickname'], font=self.title_font, fill=1)
        
        # Second line: Last online time with smaller font
        last_logoff = f"最后在线: {steam_data['last_logoff']}"
        draw.text((10, 35), last_logoff, font=ImageFont.truetype(os.path.join('assets','simhei.ttc'), 14), fill=1)
        
        # First dividing line - full width
        draw.line([(0, 60), (400, 60)], fill=1, width=1)
        
        # Stats section with reduced height
        stat_width = 400 // 3
        
        # Vertical divider lines
        draw.line([(stat_width, 60), (stat_width, 115)], fill=1, width=1)
        draw.line([(2 * stat_width, 60), (2 * stat_width, 115)], fill=1, width=1)
        
        # Level stats - centered in first column
        level_center = stat_width // 2
        level_value = str(steam_data['steam_level'])
        level_label = "等级"
        level_value_width = draw.textlength(level_value, font=self.title_font)
        level_label_width = draw.textlength(level_label, font=self.content_font)
        # Vertically center content
        draw.text((level_center - level_value_width/2, 70), level_value, font=self.title_font, fill=1)
        draw.text((level_center - level_label_width/2, 90), level_label, font=self.content_font, fill=1)
        
        # Game time stats - centered in second column
        time_center = stat_width + stat_width // 2
        time_value = str(steam_data['total_playtime_hours'])
        time_label = "游戏时间"
        time_value_width = draw.textlength(time_value, font=self.title_font)
        time_label_width = draw.textlength(time_label, font=self.content_font)
        # Vertically center content
        draw.text((time_center - time_value_width/2, 70), time_value, font=self.title_font, fill=1)
        draw.text((time_center - time_label_width/2, 90), time_label, font=self.content_font, fill=1)
        
        # Game count stats - centered in third column
        count_center = 2 * stat_width + stat_width // 2
        count_value = str(steam_data['game_count'])
        count_label = "游戏总数"
        count_value_width = draw.textlength(count_value, font=self.title_font)
        count_label_width = draw.textlength(count_label, font=self.content_font)
        # Vertically center content
        draw.text((count_center - count_value_width/2, 70), count_value, font=self.title_font, fill=1)
        draw.text((count_center - count_label_width/2, 90), count_label, font=self.content_font, fill=1)
        
        # Second dividing line - full width (closer to first line)
        draw.line([(0, 115), (400, 115)], fill=1, width=1)
        
        # Display recent games and time
        draw.text((10, 125), "最近游戏:", font=self.content_font, fill=1)
        y = 150
        for game_name in steam_data['recent_game_names']:
            draw.text((15, y), game_name, font=self.content_font, fill=1)
            y += 20
        # 转换为24位RGB图像
        img = img.convert('RGB')
    
        return img
        
            

    def get_image_bytes(self, img):
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=95, subsampling=0)
        img_io.seek(0)
        return img_io