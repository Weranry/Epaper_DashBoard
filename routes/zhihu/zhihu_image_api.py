from flask import send_file, request
from image.zhihu.zhihu_image_creator import ZhihuImageCreator
from PIL import ImageOps

class ZhihuImageAPI:
    def __init__(self):
        self.creator = ZhihuImageCreator()

    def get_zhihu_image(self):
        # 获取请求参数
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))

        img = self.creator.create_zhihu_image()
        if img is None:
            return "获取知乎数据失败", 500

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        img_io = self.creator.get_image_bytes(img)
        return send_file(img_io, mimetype='image/jpeg') 