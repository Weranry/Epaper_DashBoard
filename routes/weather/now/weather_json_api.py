from flask import jsonify
from web.weather.weather_analysis import WeatherAnalysis
import requests

class WeatherJsonAPI:
    def get_weather_json(self, location):
        url = f"https://www.qweather.com/weather/{location}.html"
        response = requests.get(url)
        analysis = WeatherAnalysis(response.text)
        weather_data = analysis.get_weather_info()

        return jsonify(weather_data) 