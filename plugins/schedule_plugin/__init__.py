"""Schedule plugin - provides course schedule API endpoints"""
from flask import Blueprint
from .routes import schedule_json_route, schedule_image_route

# Create blueprint
blueprint = Blueprint('schedule', __name__, url_prefix='/schedule')

# Register routes
blueprint.add_url_rule('/json', view_func=schedule_json_route, methods=['GET'])
blueprint.add_url_rule('/img', view_func=schedule_image_route, methods=['GET'])
