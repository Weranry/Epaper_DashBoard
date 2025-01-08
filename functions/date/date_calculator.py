from datetime import datetime
from lunar_python import Solar, Lunar
import pytz

class DateCalculator:
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
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday = weekdays[self._now.weekday()]
        return {
            "solar_year": solar_year,
            "solar_month": solar_month,
            "solar_day": solar_day,
            "weekday": weekday
        }

    def get_lunar_date(self):
        lunar_year = self._lunar.getYearInChinese()
        lunar_month = self._lunar.getMonthInChinese() + "月"
        lunar_day = self._lunar.getDayInChinese()
        return {
            "lunar_year": lunar_year,
            "lunar_month": lunar_month,
            "lunar_day": lunar_day
        }

    def get_ganzhi_date(self):
        ganzhi_year = self._lunar.getYearInGanZhi() + "年"
        ganzhi_month = self._lunar.getMonthInGanZhi() + "月"
        ganzhi_day = self._lunar.getDayInGanZhi() + "日"
        return {
            "ganzhi_year": ganzhi_year,
            "ganzhi_month": ganzhi_month,
            "ganzhi_day": ganzhi_day
        }

    def get_season_info(self):
        wu_hou = self._lunar.getWuHou()
        hou = self._lunar.getHou()
        shu_jiu = self._lunar.getShuJiu()
        fu = self._lunar.getFu()
        FuJiu = f"{shu_jiu}" if shu_jiu else f"{fu}" if fu else ""
        return {
            "wu_hou": wu_hou,
            "hou": hou,
            "fujiu": FuJiu
        }

    def get_festival_info(self):
        solar_festivals = self._solar.getFestivals()
        solar_other_festivals = self._solar.getOtherFestivals()
        lunar_festivals = self._lunar.getFestivals()
        lunar_other_festivals = self._lunar.getOtherFestivals()
        return {
            "solar_festival": " ".join(solar_festivals + solar_other_festivals),
            "lunar_festival": " ".join(lunar_festivals + lunar_other_festivals)
        } 