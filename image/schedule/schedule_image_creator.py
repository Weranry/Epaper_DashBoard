from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

class ScheduleImageCreator:
    def __init__(self):
        font_path = os.path.join('assets', 'simhei.ttc')
        self.title_font = ImageFont.truetype(font_path, 24)
        self.subtitle_font = ImageFont.truetype(font_path, 20)
        self.content_font = ImageFont.truetype(font_path, 17)

    def create_schedule_image(self, schedule_data):
        # 创建一个400x300的索引颜色图片，使用黑、白、红三色调色板
        img = Image.new('P', (400, 300))
        img.putpalette([
            255, 255, 255,  # 白色 (0)
            0, 0, 0,        # 黑色 (1)
            255, 0, 0       # 红色 (2)
        ])

        draw = ImageDraw.Draw(img)
        
        # 使用白色作为背景
        draw.rectangle([(0, 0), (400, 300)], fill=0)

        date_values = list(schedule_data['dateInfo'].values())
        # 第一行显示周次
        first_line = f"{date_values[1]} {date_values[2]}"
        draw.text((20, 5), first_line , font=self.title_font, fill=1)
        
        # 第二行显示日期
        draw.text((20, 35), date_values[0], font=self.subtitle_font, fill=1)

        # 绘制主分隔线
        draw.line([(20, 65), (380, 65)], fill=1, width=2)

        # 绘制课程信息
        y_position = 65
        spacing = 47  # 课程间距
        
        course_labels = ["Af", "As", "Pf", "Ps", "Ev"]
        for i, label in enumerate(course_labels, start=1):
            # 显示课序号
            course_number = f"{label}. "
            draw.text((20, y_position), course_number, 
                     font=self.subtitle_font, fill=1)
            
            course = schedule_data['schedule'][f'course{i}']
            if course['name']:
                # 课程名称，添加书名号
                course_name = f"《{course['name']}》"
                draw.text((45, y_position), course_name, 
                         font=self.content_font, fill=1)
                
                # 教室和教师信息
                details = f"@{course['room']} by {course['teacher']}"
                draw.text((40, y_position + 22), details, 
                         font=self.content_font, fill=1)
            
            # 在每节课后添加分隔线（最后一节课后不加）
            if i < 5:
                draw.line([(20, y_position + spacing - 2), (380, y_position + spacing - 2)], 
                         fill=1, width=1)
            
            y_position += spacing

        # 转换为24位RGB图像
        img = img.convert('RGB')
        return img

    def get_image_bytes(self, img):
        img_io = BytesIO()
        # 保存为JPEG，使用最高质量
        img.save(img_io, 'JPEG', quality=95, subsampling=0)  # 4:4:4 subsampling
        img_io.seek(0)
        return img_io