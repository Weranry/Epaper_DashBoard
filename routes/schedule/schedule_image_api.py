from flask import send_file, request
from lib.schedule.schedule_parser import ScheduleParser
from image.schedule.schedule_image_creator import ScheduleImageCreator
from PIL import ImageOps

class ScheduleImageAPI:
    def __init__(self, json_file_path):
        self.parser = ScheduleParser(json_file_path)
        self.creator = ScheduleImageCreator()

    def get_schedule_image(self):
        # 获取请求参数
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))

        schedule_data = self.parser.get_today_schedule()
        img = self.creator.create_schedule_image(schedule_data)

        # 处理反色
        if invert:
            img = ImageOps.invert(img.convert('RGB'))

        # 处理旋转
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)

        img_io = self.creator.get_image_bytes(img)
        return send_file(img_io, mimetype='image/jpeg') 