from flask import send_file, request
from lib.date.today_huangli_A import todayhuangliA
from image.date.today_huangli_image_A_creator import huangliImageACreator
from PIL import ImageOps

class huangliImageAAPI:
    def __init__(self):
        self.huangliA = todayhuangliA()
        self.creator = huangliImageACreator()

    def get_huangli_A_image(self):
        # 获取请求参数
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))

        date_data = {
            'solar': self.huangliA.get_solar_date(),
            'lunar': self.huangliA.get_lunar_date(),
            'ganzhi': self.huangliA.get_ganzhi_date(),
            'yiji': self.huangliA.get_Day_Yiji()
        }
        
        img = self.creator.create_huangli_A_image(date_data)

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        img_io = self.creator.get_image_bytes(img)
        
        return send_file(img_io, mimetype='image/jpeg') 