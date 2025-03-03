import sys
sys.dont_write_bytecode = True

from flask import Flask, send_from_directory
from routes.date.date_info_api import DateInfoAPI
from routes.date.date_image_api import DateImageAPI
from routes.weather.now.weather_json_api import WeatherJsonAPI
from routes.weather.now.weather_image_api import WeatherImageAPI
from routes.schedule.schedule_json_api import ScheduleJsonAPI
from routes.schedule.schedule_image_api import ScheduleImageAPI
from routes.zhihu.zhihu_image_api import ZhihuImageAPI
from routes.mmc_calendar.mmc_calendar_api import MMCImageAPI
from routes.date.month_image_api import MonthImageAPI
from routes.steam.steam_image_api import SteamImageAPI
from routes.date.today_huangli_image_api import huangliImageAPI


app = Flask(__name__)

# 实例化API类
date_info_api = DateInfoAPI()
date_image_api = DateImageAPI()
weather_json_api = WeatherJsonAPI()
weather_image_api = WeatherImageAPI()
schedule_json_api = ScheduleJsonAPI('data/course.json')  # 更新为实际路径
schedule_image_api = ScheduleImageAPI('data/course.json')  # 更新为实际路径
zhihu_image_api = ZhihuImageAPI()
mmc_image_api = MMCImageAPI()
month_image_api = MonthImageAPI()
steam_image_api = SteamImageAPI()
huangli_image_api = huangliImageAPI()

# 注册路由
app.add_url_rule('/date/json', view_func=date_info_api.get_date_info, methods=['GET'])
app.add_url_rule('/date/img', view_func=date_image_api.get_date_image, methods=['GET'])
app.add_url_rule('/weather/now/json/<location>', view_func=weather_json_api.get_weather_json, methods=['GET'])
app.add_url_rule('/weather/now/img/<location>', view_func=weather_image_api.get_weather_image, methods=['GET'])
app.add_url_rule('/zhihu/img', view_func=zhihu_image_api.get_zhihu_image, methods=['GET'])
app.add_url_rule('/MMC/<int:channel>', view_func=mmc_image_api.get_mmc_image, methods=['GET'])
app.add_url_rule('/date/monthimg', view_func=month_image_api.get_month_image, methods=['GET'])
app.add_url_rule('/Steam/getimg/<api_key>/<steam_id>', view_func=steam_image_api.get_steam_image, methods=['GET'])
app.add_url_rule('/schedule/json', view_func=schedule_json_api.get_schedule_json, methods=['GET'])
app.add_url_rule('/schedule/img', view_func=schedule_image_api.get_schedule_image, methods=['GET'])
app.add_url_rule('/date/huangli/b', view_func=huangli_image_api.get_huangli_image,methods=['GET'])

# 添加 favicon.ico 路由
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)#使用本地服务器调试 + vercel 部署选这个
    #app.run(host='0.0.0.0', port=5000, debug=True)#使用本地 + 局域网服务器调试