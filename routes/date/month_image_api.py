from flask import send_file, request
from image.date.month_image_creator import MonthImageCreator
from PIL import ImageOps
from datetime import datetime

class MonthImageAPI:
    def __init__(self):
        self.creator = MonthImageCreator()
        
    def get_month_image(self):
        # 获取请求参数
        year = int(request.args.get('year', datetime.now().year))
        month = int(request.args.get('month', datetime.now().month))
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))
        # 新参数：first_day，值为'sun'或'mon'，默认为'mon'
        first_day = request.args.get('first_day', 'mon').lower()
        
        # 验证first_day参数
        if first_day not in ['sun', 'mon']:
            first_day = 'mon'  # 如果参数无效，默认使用'mon'

        # 生成月历图像
        img = self.creator.draw_month_calendar(year, month, first_day)

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        # 将图像保存到内存中的字节流
        img_io = self.creator.get_image_bytes(img)
        return send_file(img_io, mimetype='image/jpeg') 