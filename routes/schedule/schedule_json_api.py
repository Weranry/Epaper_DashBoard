from flask import jsonify
from functions.schedule.schedule_parser import ScheduleParser

class ScheduleJsonAPI:
    def __init__(self, json_file_path):
        self.parser = ScheduleParser(json_file_path)

    def get_schedule_json(self):
        schedule_data = self.parser.get_today_schedule()
        return jsonify(schedule_data) 