from flask import send_file, request
from web.weather.weather_analysis import WeatherAnalysis
from image.weather.weather_image_creator import WeatherImageCreator
import requests
from PIL import ImageOps

class WeatherImageAPI:
    def __init__(self):
        self.creator = WeatherImageCreator()

    def get_weather_image(self, location):
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))

        url = f"https://www.qweather.com/weather/{location}.html"
        response = requests.get(url)
        analysis = WeatherAnalysis(response.text)
        weather_data = analysis.get_weather_info()

        img = self.creator.create_weather_image(weather_data)

        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        img_io = self.creator.get_image_bytes(img)

        return send_file(img_io, mimetype='image/jpeg') 