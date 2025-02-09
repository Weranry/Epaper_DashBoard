from flask import send_file, request
from image.date.month_image_creator import draw_month_calendar, get_image_bytes
from PIL import ImageOps
from datetime import datetime

class MonthImageAPI:
    def get_month_image(self):
        # 获取请求参数
        year = int(request.args.get('year', datetime.now().year))
        month = int(request.args.get('month', datetime.now().month))
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))

        # 生成月历图像
        img = draw_month_calendar(year, month)

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        # 将图像保存到内存中的字节流
        img_io = get_image_bytes(img)
        return send_file(img_io, mimetype='image/jpeg') 