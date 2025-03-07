from flask import send_file, jsonify, request
from web.mmc_calendar.mmc_calendar_fetcher import fetch_mmc_calendar_image
from image.mmc_calendar.mmc_calendar_image_creator import create_mmc_calendar_image
import requests
import datetime
import io  # 导入io模块以处理内存中的图像
from PIL import ImageOps  # 添加 ImageOps

class MMCImageAPI:
    def get_mmc_image(self, channel):
        # 获取请求参数
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))

        image_url = fetch_mmc_calendar_image(channel)
        if image_url is None:
            return jsonify({"error": "失败的请求，请检查频道号是否正确"}), 404

        # 下载图像数据
        response = requests.get(image_url)
        image_data = response.content

        # 创建图像
        img = create_mmc_calendar_image(image_data)

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        # 将图像保存到内存中的字节流
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)  # 将指针移动到字节流的开头

        return send_file(img_byte_arr, mimetype='image/jpeg') 