from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

class ScheduleImageCreator:
    def __init__(self):
        font_path = os.path.join('assets', 'simhei.ttc')
        self.font = ImageFont.truetype(font_path, 18)

    def create_schedule_image(self, schedule_data):
        img = Image.new('RGB', (400, 300), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        # 绘制日期信息
        y_position = 10
        for key, value in schedule_data['dateInfo'].items():
            draw.text((10, y_position), f"{key}: {value}", font=self.font, fill=(0, 0, 0))
            y_position += 20

        # 绘制课程表
        y_position += 10
        for i in range(1, 6):
            course = schedule_data['schedule'][f'course{i}']
            draw.text((10, y_position), f"Lesson {i}: {course['name']} {course['room']} {course['teacher']}", font=self.font, fill=(0, 0, 0))
            y_position += 20

        return img

    def get_image_bytes(self, img):
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=95)
        img_io.seek(0)
        return img_io 