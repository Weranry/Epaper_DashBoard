from flask import send_file, jsonify
from web.mmc_calendar.mmc_calendar_fetcher import fetch_mmc_calendar_image
from image.mmc_calendar.mmc_calendar_image_creator import create_mmc_calendar_image
import requests
import datetime
import os

class MMCImageAPI:
    def get_mmc_image(self, channel):
        image_url = fetch_mmc_calendar_image(channel)
        if image_url is None:
            return jsonify({"error": "失败的请求，请检查频道号是否正确"}), 404

        # 下载图像数据
        response = requests.get(image_url)
        image_data = response.content

        # 创建图像
        img = create_mmc_calendar_image(image_data)

        # 生成文件名
        today = datetime.datetime.now()
        filename = f"{channel}_{today.strftime('%y%m%d')}.jpeg"

        # 保存图像为JPEG格式
        output_path = os.path.join(os.path.dirname(__file__), filename)
        img.save(output_path, 'JPEG')

        return send_file(output_path, mimetype='image/jpeg') 