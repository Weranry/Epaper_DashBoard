from flask import send_file, request
from web.steam.get_steam import get_steam_data
from image.steam.steam_image_creator import SteamImageCreator
from PIL import ImageOps


class SteamImageAPI:
    def __init__(self):
        self.creator = SteamImageCreator()

    def get_steam_image(self, api_key, steam_id):
        # 获取请求参数
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))


        steam_data = get_steam_data(api_key, steam_id)


        img = self.creator.create_steam_image(steam_data)

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)


        img_io = self.creator.get_image_bytes(img)


        return send_file(img_io, mimetype='image/jpeg')