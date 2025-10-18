"""Miscellaneous plugin - provides various API endpoints"""
from flask import Blueprint
from .routes import (zhihu_image_route, mmc_calendar_route, steam_image_route,
                     wiki_image_route, sunnyclock_image_route, oneway_image_route)

# Create blueprint
blueprint = Blueprint('misc', __name__)

# Register routes
blueprint.add_url_rule('/zhihu/img', view_func=zhihu_image_route, methods=['GET'])
blueprint.add_url_rule('/miaomiaoce/<int:channel>', view_func=mmc_calendar_route, methods=['GET'])
blueprint.add_url_rule('/Steam/getimg/<api_key>/<steam_id>', view_func=steam_image_route, methods=['GET'])
blueprint.add_url_rule('/wiki/img', view_func=wiki_image_route, methods=['GET'])
blueprint.add_url_rule('/sunnyclock/<float:lat>/<float:lon>', view_func=sunnyclock_image_route, methods=['GET'])
blueprint.add_url_rule('/oneway', view_func=oneway_image_route, methods=['GET'])
