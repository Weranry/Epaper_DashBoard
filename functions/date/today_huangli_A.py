from datetime import datetime
from lunar_python import Solar, Lunar
import pytz

class todayhuangliA:
    def __init__(self, timezone='Asia/Shanghai'):
        # 设置时区
        self.timezone = pytz.timezone(timezone)
        self._now = datetime.now(self.timezone)
        self._solar = Solar.fromDate(self._now)
        self._lunar = Lunar.fromDate(self._now)
    
    def get_solar_date(self):
        solar_year = str(self._solar.getYear())
        solar_month = str(self._solar.getMonth()).zfill(2)
        solar_day = str(self._solar.getDay()).zfill(2)
        xingzuo = str(self._solar.getXingZuo()) + "座"
        # 获取星期几
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekday = weekdays[self._now.weekday()]
        return {
            "solar_year": solar_year,
            "solar_month": solar_month,
            "solar_day": solar_day,
            "weekday": weekday,
            "xingzuo" : xingzuo
        }

    def get_lunar_date(self):
        lunar_month = self._lunar.getMonthInChinese() + "月"
        lunar_day = self._lunar.getDayInChinese()
        return {
            "lunar_month": lunar_month,
            "lunar_day": lunar_day
        }

    def get_ganzhi_date(self):
        ganzhi_year = self._lunar.getYearInGanZhi() + "年"
        ganzhi_month = self._lunar.getMonthInGanZhi() + "月"
        ganzhi_day = self._lunar.getDayInGanZhi() + "日"
        shengxiao = self._lunar.getYearShengXiao()
        return {
            "ganzhi_year": ganzhi_year,
            "ganzhi_month": ganzhi_month,
            "ganzhi_day": ganzhi_day,
            "shengxiao": shengxiao
        }
    
    def get_Day_Yiji(self):
        Day_Yi = self._lunar.getDayYi()
        Day_Ji = self._lunar.getDayJi()
        return {
            "Yi": Day_Yi,
            "Ji": Day_Ji
        }