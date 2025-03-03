from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

class huangliImageCreator:
    def __init__(self):
        font_path = os.path.join('assets', 'simhei.ttc')
        self.font = ImageFont.truetype(font_path, 16)
        self.small_font = ImageFont.truetype(font_path, 14)

    def create_huangli_image(self, date_data):
        # Create a 400x300 indexed color image with a palette of white, black, and red
        img = Image.new('P', (400, 300))
        img.putpalette([
            255, 255, 255,  # White
            0, 0, 0,        # Black
            255, 0, 0       # Red
        ])
        draw = ImageDraw.Draw(img)

        # Draw horizontal lines to separate three main sections
        draw.line([(0, 100), (400, 100)], fill=1, width=1)
        draw.line([(0, 200), (400, 200)], fill=1, width=1)

        # Top section: Draw vertical lines to create 5 equal parts
        for x in range(80, 400, 80):
            draw.line([(x, 0), (x, 100)], fill=1, width=1)

        # Middle section: Draw vertical lines to create 4 equal parts
        for x in range(100, 400, 100):
            draw.line([(x, 100), (x, 200)], fill=1, width=1)

        # Draw jishen in the top section
        jishen = date_data['jishen']
        for i, (key, value) in enumerate(jishen.items()):
            x = i * 80 + 40
            draw.text((x, 30), key, fill=1, font=self.font, anchor='mm')
            draw.text((x, 70), value, fill=1, font=self.font, anchor='mm')

        # Draw other parameters in the middle section
        middle_items = [
            ('太岁', date_data['ganzhi']),
            ('胎神', date_data['taishen']),
            ('冲煞', date_data['chongsha']),
            ('二十八宿', date_data['ershibaxingxiu'])
        ]

        for i, (key, value) in enumerate(middle_items):
            x = i * 100 + 50
            draw.text((x, 120), key, fill=1, font=self.font, anchor='mm')
            draw.text((x, 160), value, fill=1, font=self.small_font, anchor='mm')

        # Draw pengzubaiji in the bottom section
        draw.text((200, 220), "彭祖百忌", fill=1, font=self.font, anchor='mm')
        draw.text((200, 260), date_data['pengzubaiji'], fill=1, font=self.small_font, anchor='mm')

        # Convert to RGB mode
        img = img.convert('RGB')
        return img

    def get_image_bytes(self, img):
        img_io = BytesIO()
        # Save as JPEG with maximum quality and 4:4:4 subsampling
        img.save(img_io, 'JPEG', quality=95, subsampling=0)
        img_io.seek(0)
        return img_io

