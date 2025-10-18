"""Schedule plugin routes"""
from core.base_api import BaseImageAPI, BaseJsonAPI
from lib.schedule.schedule_parser import ScheduleParser
from image.schedule.schedule_image_creator import ScheduleImageCreator
from flask import jsonify


class ScheduleJsonAPI(BaseJsonAPI):
    """API for schedule information in JSON format"""
    def __init__(self, json_file_path='data/course.json'):
        super().__init__()
        self.parser = ScheduleParser(json_file_path)
    
    def get_schedule_json(self):
        schedule_data = self.parser.get_today_schedule()
        return jsonify(schedule_data)


class ScheduleImageAPI(BaseImageAPI):
    """API for schedule image"""
    def __init__(self, json_file_path='data/course.json'):
        super().__init__()
        self.parser = ScheduleParser(json_file_path)
        self.creator = ScheduleImageCreator()
    
    def get_schedule_image(self):
        schedule_data = self.parser.get_today_schedule()
        img = self.creator.create_schedule_image(schedule_data)
        return self.process_and_send_image(img)


# Create route instances
schedule_json_api = ScheduleJsonAPI()
schedule_image_api = ScheduleImageAPI()

# Export route functions
schedule_json_route = schedule_json_api.get_schedule_json
schedule_image_route = schedule_image_api.get_schedule_image
