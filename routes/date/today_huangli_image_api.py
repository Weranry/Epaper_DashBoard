from flask import send_file, request
from lib.date.today_huangli import todayhuangli
from image.date.today_huangli_image_creator import huangliImageCreator
from PIL import ImageOps

class huangliImageAPI:
    def __init__(self):
        self.huangli = todayhuangli()
        self.creator = huangliImageCreator()

    def get_huangli_image(self):
        # 获取请求参数
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))

        date_data = {
            'jishen': self.huangli.get_jishen(),
            'taishen': self.huangli.get_taishen(),
            'ganzhi': self.huangli.get_taisui(),
            'pengzubaiji': self.huangli.get_pengzubaiji(),
            'ershibaxingxiu': self.huangli.get_ershibaxingxiu(),
            'chongsha': self.huangli.get_chongsha()
        }
        
        img = self.creator.create_huangli_image(date_data)

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        img_io = self.creator.get_image_bytes(img)
        
        return send_file(img_io, mimetype='image/jpeg') 