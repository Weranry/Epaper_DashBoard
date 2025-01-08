from flask import send_file
from image.zhihu.zhihu_image_creator import ZhihuImageCreator

class ZhihuImageAPI:
    def __init__(self):
        self.creator = ZhihuImageCreator()

    def get_zhihu_image(self):
        img = self.creator.create_zhihu_image()
        if img is None:
            return "获取知乎数据失败", 500

        img_io = self.creator.get_image_bytes(img)
        return send_file(img_io, mimetype='image/jpeg') 