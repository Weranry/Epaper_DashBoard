"""Miscellaneous plugin routes"""
from core.base_api import BaseImageAPI
from image.zhihu.zhihu_image_creator import ZhihuImageCreator
from image.mmc_calendar.mmc_calendar_image_creator import create_mmc_calendar_image
from web.mmc_calendar.mmc_calendar_fetcher import fetch_mmc_calendar_image
from image.steam.steam_image_creator import SteamImageCreator
from image.wiki.wiki_image_generator import WikiImageCreator
from image.sunnyclock.sunnyclock_image_creator import SunnyClockImageCreator
from image.one_way.one_way_image_creator import create_one_way_image
from web.one_way.one_way_fetcher import fetch_one_way_image
from flask import request
import requests


class ZhihuImageAPI(BaseImageAPI):
    """API for Zhihu hot topics image"""
    def __init__(self):
        super().__init__()
        self.creator = ZhihuImageCreator()
    
    def get_zhihu_image(self):
        img = self.creator.create_zhihu_image()
        if img is None:
            return "Failed to fetch Zhihu data", 500
        return self.process_and_send_image(img)


class MMCImageAPI(BaseImageAPI):
    """API for MiaoMiaoCe calendar image"""
    def __init__(self):
        super().__init__()
    
    def get_mmc_image(self, channel):
        image_url = fetch_mmc_calendar_image(channel)
        if image_url is None:
            return "Failed to fetch MiaoMiaoCe data", 404
        
        # Download image data
        response = requests.get(image_url)
        image_data = response.content
        
        # Create image
        img = create_mmc_calendar_image(image_data)
        return self.process_and_send_image(img)


class SteamImageAPI(BaseImageAPI):
    """API for Steam game info image"""
    def __init__(self):
        super().__init__()
        self.creator = SteamImageCreator()
    
    def get_steam_image(self, api_key, steam_id):
        img = self.creator.create_steam_image(api_key, steam_id)
        if img is None:
            return "Failed to fetch Steam data", 500
        return self.process_and_send_image(img)


class WikiImageAPI(BaseImageAPI):
    """API for Wikipedia featured article image"""
    def __init__(self):
        super().__init__()
        self.creator = WikiImageCreator()
    
    def get_wiki_image(self):
        height = request.args.get('height', default=800, type=int)
        img = self.creator.create_wiki_image(height)
        if img is None:
            return "Failed to fetch Wikipedia data", 500
        return self.process_and_send_image(img)


class SunnyClockImageAPI(BaseImageAPI):
    """API for Sunny Clock astronomical image"""
    def __init__(self):
        super().__init__()
        self.creator = SunnyClockImageCreator()
    
    def get_sunnyclock_image(self, lat, lon):
        img = self.creator.create_sunnyclock_image(lat, lon)
        if img is None:
            return "Failed to fetch Sunny Clock data", 500
        return self.process_and_send_image(img)


class OneWayImageAPI(BaseImageAPI):
    """API for OneWay daily quote image"""
    def __init__(self):
        super().__init__()
    
    def get_one_way_image(self):
        # Fetch the image content
        image_data = fetch_one_way_image()
        
        if image_data is None:
            return "Failed to fetch OneWay data", 404
        
        # Get common params (invert, rotate)
        params = self.get_common_params()
        
        # Process the image
        img = create_one_way_image(image_data, params['invert'], params['rotate'])
        
        if img is None:
            return "Failed to process OneWay image", 500
        
        # Send without further processing (already processed by create_one_way_image)
        img_io = self.image_processor.get_image_bytes(img)
        from flask import send_file
        return send_file(img_io, mimetype='image/jpeg')


# Create route instances
zhihu_image_api = ZhihuImageAPI()
mmc_calendar_api = MMCImageAPI()
steam_image_api = SteamImageAPI()
wiki_image_api = WikiImageAPI()
sunnyclock_image_api = SunnyClockImageAPI()
oneway_image_api = OneWayImageAPI()

# Export route functions
zhihu_image_route = zhihu_image_api.get_zhihu_image
mmc_calendar_route = mmc_calendar_api.get_mmc_image
steam_image_route = steam_image_api.get_steam_image
wiki_image_route = wiki_image_api.get_wiki_image
sunnyclock_image_route = sunnyclock_image_api.get_sunnyclock_image
oneway_image_route = oneway_image_api.get_one_way_image
