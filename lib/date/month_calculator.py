import calendar
from datetime import datetime
from zhdate import ZhDate

def get_calendar_data(year, month, is_sunday_first=False):
    # 设置日历首日
    if is_sunday_first:
        calendar.setfirstweekday(6)  # 6 表示周日为一周的第一天
    else:
        calendar.setfirstweekday(0)  # 0 表示周一为一周的第一天
    
    cal = calendar.monthcalendar(year, month)
    return cal

def get_lunar_date(year, month, day):
    lunar_date = ZhDate.from_datetime(datetime(year, month, day))
    lunar_str = lunar_date.chinese()
    if lunar_str[9] in '一二三四五六七八九':
        lunar_str = lunar_str[:7] + '廿' + lunar_str[9:]  # 替换第八九位为廿
    if "初一" in lunar_str:
        return lunar_str[5:7]  # 返回月份
    else:
        return lunar_str[7:9]  # 返回日期 