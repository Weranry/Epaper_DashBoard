from flask import send_file, request
from image.sunnyclock.sunnyclock_image_creator import SunnyClockImageCreator
from PIL import ImageOps

class SunnyClockImageAPI:
    def __init__(self):
        self.creator = SunnyClockImageCreator()

    def get_sunnyclock_image(self, lat, lon):
        # 获取请求参数
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))

        img = self.creator.create_sunnyclock_image(lat, lon)
        if img is None:
            return "获取晴天钟数据失败", 500

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        img_io = self.creator.get_image_bytes(img)
        return send_file(img_io, mimetype='image/jpeg')