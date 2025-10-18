"""Date plugin - provides date-related API endpoints"""
from flask import Blueprint
from .routes import date_info_route, date_image_route, month_image_route
from .routes import huangli_b_route, huangli_a_route

# Create blueprint
blueprint = Blueprint('date', __name__, url_prefix='/date')

# Register routes
blueprint.add_url_rule('/json', view_func=date_info_route, methods=['GET'])
blueprint.add_url_rule('/img', view_func=date_image_route, methods=['GET'])
blueprint.add_url_rule('/monthimg', view_func=month_image_route, methods=['GET'])
blueprint.add_url_rule('/huangli/b', view_func=huangli_b_route, methods=['GET'])
blueprint.add_url_rule('/huangli/a', view_func=huangli_a_route, methods=['GET'])
