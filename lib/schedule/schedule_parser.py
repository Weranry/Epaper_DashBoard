import json
from datetime import datetime
import pytz

class ScheduleParser:
    def __init__(self, json_file_path, timezone='Asia/Shanghai'):
        self.timezone = pytz.timezone(timezone)
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.courses = data['courses']
            self.semester_start = datetime.strptime(
                data['semesterStartDate'], 
                '%Y-%m-%d'
            ).replace(tzinfo=self.timezone)

    def get_today_schedule(self):
        current_date = datetime.now(self.timezone)
        week_number = ((current_date - self.semester_start).days // 7) + 1
        day_of_week = current_date.isoweekday()

        today_schedule = [{'lesson': i, 'course': {}} for i in range(1, 6)]

        for course in self.courses:
            for classroom in course['classroom']:
                if classroom['dayOfWeek'] == day_of_week and week_number in classroom['week']:
                    today_schedule[classroom['lesson'] - 1]['course'] = {
                        'name': course['courseName'],
                        'room': classroom['room'],
                        'teacher': course['teacher']
                    }

        date_info = {
            'todayDate': current_date.strftime('%Y年%m月%d日'),
            'weekNumber': f'第{week_number}周',
            'dayOfWeek': ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][day_of_week - 1]
        }

        formatted_schedule = {
            f'course{i}': {
                'name': today_schedule[i - 1]['course'].get('name', ''),
                'room': today_schedule[i - 1]['course'].get('room', ''),
                'teacher': today_schedule[i - 1]['course'].get('teacher', '')
            } for i in range(1, 6)
        }

        return {'dateInfo': date_info, 'schedule': formatted_schedule}