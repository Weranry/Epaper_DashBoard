from PIL import Image, ImageDraw, ImageFont
from functions.date.month_calculator import get_calendar_data, get_lunar_date
from io import BytesIO
import os
from datetime import datetime

def draw_month_calendar(year, month):
    # 创建一个新的白色背景图像
    img = Image.new('P', (400, 300))
    img.putpalette([
        255, 255, 255,  # 白色
        0, 0, 0,        # 黑色
        255, 0, 0       # 红色
    ])
    d = ImageDraw.Draw(img)

    # 加载字体，增大字体大小
    font_path = os.path.join('assets', 'simhei.ttc')
    title_font = ImageFont.truetype(font_path, 24)  # 增大标题字体
    weekday_font = ImageFont.truetype(font_path, 18)  # 增大星期字体
    day_font = ImageFont.truetype(font_path, 20)  # 增大日期字体
    lunar_font = ImageFont.truetype(font_path, 16)  # 增大农历字体

    # 绘制标题
    title = f"{year}年{month}月"
    d.text((200, 10), title, font=title_font, fill=1, anchor='mt')

    # 绘制星期
    weekdays = ['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun']
    for i, day in enumerate(weekdays):
        d.text((50 + i * 50, 40), day, font=weekday_font, fill=1, anchor='mt')

    # 绘制横线
    d.line([(0, 37), (400, 37)], fill=1, width=1)  # 上方横线
    d.line([(0, 57), (400, 57)], fill=1, width=1)  # 下方横线

    # 获取日历数据
    cal_data = get_calendar_data(year, month)

    # 获取今天的日期
    today = datetime.now()
    today_day = today.day if today.year == year and today.month == month else None

    # 绘制日期
    for week_num, week in enumerate(cal_data):
        for day_num, day in enumerate(week):
            if day != 0:
                x = 50 + day_num * 50
                y = 80 + week_num * 40

                # 如果是今天，绘制一个黑色方框
                if day == today_day:
                    d.rectangle([x-20, y-5, x+20, y+37],  outline=1, width=1)  # 使用黑色框

                d.text((x, y), str(day), font=day_font, fill=1, anchor='mt')
                lunar_day = get_lunar_date(year, month, day)
                d.text((x, y + 20), lunar_day, font=lunar_font, fill=1, anchor='mt')

    # 转换为24位RGB图像
    img = img.convert('RGB')
    
    return img

def get_image_bytes(img):
    img_io = BytesIO()
    # 保存为JPEG，使用最高质量
    img.save(img_io, 'JPEG', quality=95, subsampling=0)  # 4:4:4 subsampling
    img_io.seek(0)
    return img_io 