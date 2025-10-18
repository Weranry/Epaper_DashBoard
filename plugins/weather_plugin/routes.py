"""Weather plugin routes"""
from core.base_api import BaseImageAPI, BaseJsonAPI
from web.weather.weather_analysis import WeatherAnalysis
from image.weather.weather_image_creator import WeatherImageCreator
from lib.Weather_landscape.weather_landscape_view import WeatherDrawer
from lib.Weather_landscape.weather_landscape_fetcher import WeatherData
from flask import jsonify, request
import requests
import random
import datetime


class WeatherJsonAPI(BaseJsonAPI):
    """API for weather information in JSON format"""
    def __init__(self):
        super().__init__()
    
    def get_weather_json(self, location):
        url = f"https://www.qweather.com/weather/{location}.html"
        response = requests.get(url)
        analysis = WeatherAnalysis(response.text)
        weather_data = analysis.get_weather_info()
        return jsonify(weather_data)


class WeatherImageAPI(BaseImageAPI):
    """API for weather image"""
    def __init__(self):
        super().__init__()
        self.creator = WeatherImageCreator()
    
    def get_weather_image(self, location):
        url = f"https://www.qweather.com/weather/{location}.html"
        response = requests.get(url)
        analysis = WeatherAnalysis(response.text)
        weather_data = analysis.get_weather_info()
        
        img = self.creator.create_weather_image(weather_data)
        return self.process_and_send_image(img)


class WeatherLandscapeAPI(BaseImageAPI):
    """API for weather landscape visualization"""
    def __init__(self):
        super().__init__()
    
    def get_weather_landscape_image(self, lat, lon, key):
        units = request.args.get('units', default=0, type=int)
        pressure_min = request.args.get('pressure_min', default=980, type=float)
        pressure_max = request.args.get('pressure_max', default=1030, type=float)
        
        # Set random seed for consistent image generation
        current_hour = int(datetime.datetime.now().strftime('%Y%m%d%H'))
        random.seed(current_hour)
        
        # Fetch weather data
        weather_data = WeatherData(key, lat, lon, units, pressure_min, pressure_max)
        weather_data.get_weather_data()
        
        # Generate image
        drawer = WeatherDrawer()
        img = drawer.draw_weather(weather_data)
        
        return self.process_and_send_image(img)


# Create route instances
weather_json_api = WeatherJsonAPI()
weather_image_api = WeatherImageAPI()
weather_landscape_api = WeatherLandscapeAPI()

# Export route functions
weather_json_route = weather_json_api.get_weather_json
weather_image_route = weather_image_api.get_weather_image
weather_landscape_route = weather_landscape_api.get_weather_landscape_image
