"""Weather plugin - provides weather-related API endpoints"""
from flask import Blueprint
from .routes import weather_json_route, weather_image_route, weather_landscape_route

# Create blueprint
blueprint = Blueprint('weather', __name__, url_prefix='/weather')

# Register routes
blueprint.add_url_rule('/now/json/<location>', view_func=weather_json_route, methods=['GET'])
blueprint.add_url_rule('/now/img/<location>', view_func=weather_image_route, methods=['GET'])
blueprint.add_url_rule('/landscape/<float:lat>/<float:lon>/<key>', view_func=weather_landscape_route, methods=['GET'])
