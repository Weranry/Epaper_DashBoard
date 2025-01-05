from flask import send_file
from functions.schedule.schedule_parser import ScheduleParser
from image.schedule.schedule_image_creator import ScheduleImageCreator

class ScheduleImageAPI:
    def __init__(self, json_file_path):
        self.parser = ScheduleParser(json_file_path)
        self.creator = ScheduleImageCreator()

    def get_schedule_image(self):
        schedule_data = self.parser.get_today_schedule()
        img = self.creator.create_schedule_image(schedule_data)
        img_io = self.creator.get_image_bytes(img)
        return send_file(img_io, mimetype='image/jpeg') 