from flask import send_file, request
from lib.date.date_calculator import DateCalculator
from image.date.date_image_creator import DateImageCreator
from PIL import ImageOps

class DateImageAPI:
    def __init__(self):
        self.calculator = DateCalculator()
        self.creator = DateImageCreator()

    def get_date_image(self):
        # 获取请求参数
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))

        date_data = {
            'solar': self.calculator.get_solar_date(),
            'lunar': self.calculator.get_lunar_date(),
            'ganzhi': self.calculator.get_ganzhi_date(),
            'season': self.calculator.get_season_info(),
            'festival': self.calculator.get_festival_info()
        }
        
        img = self.creator.create_date_image(date_data)

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        img_io = self.creator.get_image_bytes(img)
        
        return send_file(img_io, mimetype='image/jpeg') 