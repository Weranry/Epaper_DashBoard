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

        # 绘制总游玩时长
        total_playtime_text = f"总游玩时长: {steam_data['total_playtime_hours']}小时"
        draw.text((10, 10), total_playtime_text, font=self.title_font, fill=1)

        # 绘制游戏总数
        game_count_text = f"游戏总数: {steam_data['game_count']}"
        draw.text((10, 38), game_count_text, font=self.title_font, fill=1)

        # 绘制最近游玩游戏数量
        recent_game_count_text = f"最近游玩游戏数量: {steam_data['recent_game_count']}"
        draw.text((10, 58), recent_game_count_text, font=self.content_font, fill=1)

        # 绘制最近游玩游戏名称
        y = 78
        for game_name in steam_data['recent_game_names']:
            draw.text((10, y), game_name, font=self.content_font, fill=1)
            y += 20

        # 合并steam.png图片
        steam_png = Image.open(os.path.join('assets', 'pic','steam.jpg')).convert('RGB')
        img.paste(steam_png, (250, 150))

        # 转换为24位RGB图像
        img = img.convert('RGB')

        return img

    def get_image_bytes(self, img):
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=95, subsampling=0)
        img_io.seek(0)
        return img_io