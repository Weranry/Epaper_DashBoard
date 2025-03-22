from flask import send_file, request
from image.wiki.wiki_image_generator import WikiImageCreator
from PIL import ImageOps

class WikiImageAPI:
    def __init__(self):
        self.creator = WikiImageCreator()

    def get_wiki_image(self):
        # 获取请求参数
        # width和height参数暂时被注释，使用固定尺寸
        # width = request.args.get('width', default=480, type=int)
        # height = request.args.get('height', default=800, type=int)
        
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))

        # 创建图像 - 现在使用固定尺寸
        img = self.creator.create_wiki_image()
        if img is None:
            return "获取维基百科数据失败", 500

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        # 获取字节流并返回
        img_io = self.creator.get_image_bytes(img)
        return send_file(img_io, mimetype='image/jpeg')