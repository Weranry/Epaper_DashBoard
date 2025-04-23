from flask import request, send_file, jsonify
import io
import sys
import os

from .weather_landscape_fetcher import WeatherData
from .weather_landscape_view import WeatherDrawer

class WeatherLandscapeAPI:
    def __init__(self):
        pass

    def get_weather_landscape_image(self, lat, lon, key):
        try:
            # 获取可选参数
            units = int(request.args.get('units', 0))
            pressure_min = float(request.args.get('pressure_min', 980))
            pressure_max = float(request.args.get('pressure_max', 1030))
            
            if not key:
                return jsonify({"error": "API key is required"}), 400
            
            # 获取天气数据
            weather_data = WeatherData(key, lat, lon, units, pressure_min, pressure_max)
            weather_data.get_weather_data()
            
            # 生成图像
            drawer = WeatherDrawer()
            img = drawer.draw_weather(weather_data)
            
            # 转换为字节流并发送
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=100, subsampling=0)
            img_byte_arr.seek(0)
            
            return send_file(img_byte_arr, mimetype='image/jpeg')
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500