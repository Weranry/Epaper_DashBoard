from PIL import Image, ImageDraw, ImageFont
from lib.date.month_calculator import get_calendar_data, get_lunar_date
from io import BytesIO
import os
from datetime import datetime

class MonthImageCreator:
    def __init__(self):
        # 初始化字体
        font_path = os.path.join('assets', 'simhei.ttc')
        self.title_font = ImageFont.truetype(font_path, 24)  # 标题字体
        self.weekday_font = ImageFont.truetype(font_path, 18)  # 星期字体
        self.day_font = ImageFont.truetype(font_path, 20)  # 日期字体
        self.lunar_font = ImageFont.truetype(font_path, 16)  # 农历字体
        
        # 布局参数，可以通过这些参数调整日期的上下左右间距
        self.image_size = (400, 300)
        self.title_position = (200, 10)
        self.weekday_start_pos = (38, 40)
        self.weekday_spacing = 55
        self.calendar_start_pos = (38, 73)
        self.week_spacing = 45
        self.day_spacing = 55
        self.lunar_offset = 20  # 农历日期相对于公历日期的垂直偏移
        
        # 定义不同首日的星期标签
        self.monday_first = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        self.sunday_first = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
    def draw_month_calendar(self, year, month, first_day='mon'):
        # 创建一个新的白色背景图像
        img = Image.new('P', self.image_size)
        img.putpalette([
            255, 255, 255,  # 白色
            0, 0, 0,        # 黑色
            255, 0, 0       # 红色
        ])
        d = ImageDraw.Draw(img)

        # 绘制标题
        title = f"{year}年{month}月"
        d.text(self.title_position, title, font=self.title_font, fill=1, anchor='mt')

        # 检查first_day参数
        is_sunday_first = (first_day.lower() == 'sun')
        
        # 绘制星期，根据参数选择从周日还是周一开始
        self._draw_weekdays(d, is_sunday_first)

        # 绘制横线
        self._draw_separator_lines(d)

        # 获取日历数据，指定首日是周日还是周一
        cal_data = get_calendar_data(year, month, is_sunday_first)

        # 获取今天的日期
        today = datetime.now()
        today_day = today.day if today.year == year and today.month == month else None

        # 绘制日期
        self._draw_calendar_days(d, cal_data, year, month, today_day)

        # 转换为24位RGB图像
        img = img.convert('RGB')
        
        return img

    def _draw_weekdays(self, d, is_sunday_first=False):
        weekdays = self.sunday_first if is_sunday_first else self.monday_first
        for i, day in enumerate(weekdays):
            x = self.weekday_start_pos[0] + i * self.weekday_spacing
            y = self.weekday_start_pos[1]
            d.text((x, y), day, font=self.weekday_font, fill=1, anchor='mt')

    def _draw_separator_lines(self, d):
        d.line([(0, 37), (self.image_size[0], 37)], fill=1, width=1)  # 上方横线
        d.line([(0, 57), (self.image_size[0], 57)], fill=1, width=1)  # 下方横线

    def _draw_calendar_days(self, d, cal_data, year, month, today_day):
        for week_num, week in enumerate(cal_data):
            for day_num, day in enumerate(week):
                if day != 0:
                    x = self.calendar_start_pos[0] + day_num * self.day_spacing
                    y = self.calendar_start_pos[1] + week_num * self.week_spacing

                    # 如果是今天，绘制一个黑色方框
                    if day == today_day:
                        self._draw_today_highlight(d, x, y)

                    # 绘制公历日期
                    d.text((x, y), str(day), font=self.day_font, fill=1, anchor='mt')
                    
                    # 绘制农历日期
                    lunar_day = get_lunar_date(year, month, day)
                    d.text((x, y + self.lunar_offset), lunar_day, font=self.lunar_font, fill=1, anchor='mt')

    def _draw_today_highlight(self, d, x, y):
        # 高亮今天的日期
        d.rectangle([x-20, y-5, x+20, y+37], outline=1, width=1)

    def get_image_bytes(self, img):
        img_io = BytesIO()
        # 保存为JPEG，使用最高质量
        img.save(img_io, 'JPEG', quality=95, subsampling=0)  # 4:4:4 subsampling
        img_io.seek(0)
        return img_io