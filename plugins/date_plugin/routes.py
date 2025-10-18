"""Date plugin routes"""
from core.base_api import BaseImageAPI, BaseJsonAPI
from lib.date.date_calculator import DateCalculator
from image.date.date_image_creator import DateImageCreator
from image.date.month_image_creator import MonthImageCreator
from image.date.today_huangli_image_creator import huangliImageCreator
from image.date.today_huangli_image_A_creator import huangliImageACreator
from flask import request, jsonify


class DateInfoAPI(BaseJsonAPI):
    """API for date information in JSON format"""
    def __init__(self):
        super().__init__()
        self.calculator = DateCalculator()
    
    def get_date_info(self):
        return jsonify({
            'solar': self.calculator.get_solar_date(),
            'lunar': self.calculator.get_lunar_date(),
            'ganzhi': self.calculator.get_ganzhi_date(),
            'season': self.calculator.get_season_info(),
            'festival': self.calculator.get_festival_info()
        })


class DateImageAPI(BaseImageAPI):
    """API for date image"""
    def __init__(self):
        super().__init__()
        self.calculator = DateCalculator()
        self.creator = DateImageCreator()
    
    def get_date_image(self):
        date_data = {
            'solar': self.calculator.get_solar_date(),
            'lunar': self.calculator.get_lunar_date(),
            'ganzhi': self.calculator.get_ganzhi_date(),
            'season': self.calculator.get_season_info(),
            'festival': self.calculator.get_festival_info()
        }
        img = self.creator.create_date_image(date_data)
        return self.process_and_send_image(img)


class MonthImageAPI(BaseImageAPI):
    """API for month calendar image"""
    def __init__(self):
        super().__init__()
        self.creator = MonthImageCreator()
    
    def get_month_image(self):
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        first_day = request.args.get('first_day', 'mon')
        
        img = self.creator.create_month_image(year, month, first_day)
        return self.process_and_send_image(img)


class HuangliImageAPI(BaseImageAPI):
    """API for Huangli (Chinese almanac) image - Version B"""
    def __init__(self):
        super().__init__()
        self.creator = huangliImageCreator()
    
    def get_huangli_image(self):
        img = self.creator.create_huangli_image()
        return self.process_and_send_image(img)


class HuangliImageAAPI(BaseImageAPI):
    """API for Huangli (Chinese almanac) image - Version A"""
    def __init__(self):
        super().__init__()
        self.creator = huangliImageACreator()
    
    def get_huangli_A_image(self):
        img = self.creator.create_huangli_A_image()
        return self.process_and_send_image(img)


# Create route instances
date_info_api = DateInfoAPI()
date_image_api = DateImageAPI()
month_image_api = MonthImageAPI()
huangli_b_api = HuangliImageAPI()
huangli_a_api = HuangliImageAAPI()

# Export route functions
date_info_route = date_info_api.get_date_info
date_image_route = date_image_api.get_date_image
month_image_route = month_image_api.get_month_image
huangli_b_route = huangli_b_api.get_huangli_image
huangli_a_route = huangli_a_api.get_huangli_A_image
