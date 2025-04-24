import json
import datetime
import requests
import pytz
from math import cos, sin, acos, asin, tan
from math import degrees as deg, radians as rad

class WeatherData:
    """整合获取天气数据的功能"""
    
    # 温度单位常量
    TEMP_UNITS_CELSIUS = 0 
    TEMP_UNITS_FAHRENHEIT = 1
    
    # 凯尔文温度转换常量
    KTOC = 273.15
    
    # 天气类型常量
    Thunderstorm = 2
    Drizzle = 3
    Rain = 5
    Snow = 6
    Atmosphere = 7
    Clouds = 8
    
    # 预报时间周期（小时）
    FORECAST_PERIOD_HOURS = 3
    
    # API URL
    OWMURL = "http://api.openweathermap.org/data/2.5/"
    
    def __init__(self, api_key, lat, lon, units_mode=0, pressure_min=980, pressure_max=1030):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.units_mode = units_mode
        self.pressure_min = pressure_min
        self.pressure_max = pressure_max
        self.weather_data = []
        self.tzoffset = (datetime.datetime.now() - datetime.datetime.utcnow()).total_seconds()/(60*60)
        
        # 构建API请求URL
        self.reqstr = f"lat={self.lat}&lon={self.lon}&mode=json&APPID={self.api_key}"
        self.url_forecast = f"{self.OWMURL}forecast?{self.reqstr}"
        self.url_current = f"{self.OWMURL}weather?{self.reqstr}"
    
    def get_weather_data(self):
        """从OpenWeatherMap API获取天气数据"""
        self.weather_data = []
        
        # 使用requests库获取当前天气
        curr_response = requests.get(self.url_current)
        curr_data = curr_response.json()
        
        # 使用requests库获取天气预报
        forecast_response = requests.get(self.url_forecast)
        forecast_data = forecast_response.json()
        
        # 处理当前天气数据
        self.weather_data.append(self._process_weather_info(curr_data))
        
        # 处理预报数据
        if 'list' in forecast_data:
            for forecast in forecast_data['list']:
                if self._check_weather_data(forecast):
                    self.weather_data.append(self._process_weather_info(forecast))
        
        return self.weather_data
    
    def _process_weather_info(self, data):
        """处理从API获取的天气数据"""
        is_celsius = self.units_mode != self.TEMP_UNITS_FAHRENHEIT
        
        weather_info = {
            'time': datetime.datetime.fromtimestamp(int(data['dt']), pytz.UTC),
            'id': int(data['weather'][0]['id']),
            'clouds': int(data['clouds'].get('all', 0)) if 'clouds' in data else 0,
            'rain': 0.0,
            'snow': 0.0,
            'windspeed': float(data['wind'].get('speed', 0.0)) if 'wind' in data else 0.0,
            'winddeg': float(data['wind'].get('deg', 0.0)) if 'wind' in data else 0.0,
            'pressure': float(data['main']['pressure']),
            'is_celsius': is_celsius
        }
        
        # 处理雨量数据
        if 'rain' in data:
            if '3h' in data['rain']:
                weather_info['rain'] = float(data['rain']['3h'])
            elif '2h' in data['rain']:
                weather_info['rain'] = float(data['rain']['2h'])
            elif '1h' in data['rain']:
                weather_info['rain'] = float(data['rain']['1h'])
        
        # 处理雪量数据
        if 'snow' in data:
            if '3h' in data['snow']:
                weather_info['snow'] = float(data['snow']['3h'])
            elif '2h' in data['snow']:
                weather_info['snow'] = float(data['snow']['2h'])
            elif '1h' in data['snow']:
                weather_info['snow'] = float(data['snow']['1h'])
        
        # 处理温度数据
        temp_kelvin = float(data['main']['temp'])
        weather_info['temp'] = self._to_celsius(temp_kelvin)
        weather_info['temp_fahrenheit'] = self._to_fahrenheit(temp_kelvin)
        
        return weather_info
    
    def _to_celsius(self, kelvin):
        """将开尔文温度转换为摄氏度"""
        return kelvin - self.KTOC
    
    def _to_fahrenheit(self, kelvin):
        """将开尔文温度转换为华氏度"""
        return (kelvin - self.KTOC) * 1.8 + 32
    
    @staticmethod
    def _check_weather_data(data):
        """检查天气数据是否有效"""
        if not ('dt' in data):
            return False
        if not ('weather' in data):
            return False
        if not ('main' in data):
            return False
        return True
    
    def ensure_localized(self, dt):
        tz = pytz.timezone('Asia/Shanghai')
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            return tz.localize(dt)
        return dt.astimezone(tz)
    
    def get_temp_range(self, max_time):
        """获取指定时间内的温度范围（时区安全）"""
        # 强制将 max_time 转为 Asia/Shanghai aware datetime
        max_time = self.ensure_localized(max_time)
        tmax = -999
        tmin = 999
        is_first = True
        for weather in self.weather_data:
            if is_first:
                is_first = False
                continue
            # 强制将 weather['time'] 转为 Asia/Shanghai aware datetime
            weather_time = self.ensure_localized(weather['time'])
            if weather_time > max_time:
                break
            if weather['temp'] > tmax:
                tmax = weather['temp']
            if weather['temp'] < tmin:
                tmin = weather['temp']
        return (tmin, tmax)
    
    def get_current(self):
        """获取当前天气数据"""
        if len(self.weather_data) == 0:
            return None
        return self.weather_data[0]
    
    def get_forecast_at_time(self, time):
        """获取指定时间的天气预报"""
        for weather in self.weather_data:
            if weather['time'] > time:
                return weather
        return None


class SunCalculator:
    """计算日出日落时间"""
    
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.tzoffset = (datetime.datetime.now() - datetime.datetime.utcnow()).total_seconds()/(60*60)
    
    def sunrise(self, when=None):
        """计算日出时间"""
        if when is None:
            when = datetime.datetime.now()
        self.__preptime(when)
        self.__calc()
        return self.__timefromdecimalday(self.sunrise_t, when)
    
    def sunset(self, when=None):
        """计算日落时间"""
        if when is None:
            when = datetime.datetime.now()
        self.__preptime(when)
        self.__calc()
        return self.__timefromdecimalday(self.sunset_t, when)
    
    def solarnoon(self, when=None):
        """计算正午时间"""
        if when is None:
            when = datetime.datetime.now()
        self.__preptime(when)
        self.__calc()
        return self.__timefromdecimalday(self.solarnoon_t, when)
    
    @staticmethod
    def __timefromdecimalday(day, when):
        hours = 24.0 * day
        h = int(hours)
        minutes = (hours - h) * 60
        m = int(minutes)
        seconds = (minutes - m) * 60
        s = int(seconds)
        return datetime.datetime(when.year, when.month, when.day, h, m, s)
    
    def __preptime(self, when):
        self.day = when.toordinal() - (734124 - 40529)
        t = when.time()
        self.time = (t.hour + t.minute/60.0 + t.second/3600.0) / 24.0
        self.timezone = self.tzoffset
    
    def __calc(self):
        timezone = self.timezone  # in hours, east is positive
        longitude = self.lon      # in decimal degrees, east is positive
        latitude = self.lat       # in decimal degrees, north is positive
        
        time = self.time  # percentage past midnight, i.e. noon is 0.5
        day = self.day    # daynumber 1=1/1/1900
        
        Jday = day + 2415018.5 + time - timezone / 24  # Julian day
        Jcent = (Jday - 2451545) / 36525    # Julian century
        
        Manom = 357.52911 + Jcent * (35999.05029 - 0.0001537 * Jcent)
        Mlong = 280.46646 + Jcent * (36000.76983 + Jcent * 0.0003032) % 360
        Eccent = 0.016708634 - Jcent * (0.000042037 + 0.0001537 * Jcent)
        Mobliq = 23 + (26 + ((21.448 - Jcent * (46.815 + Jcent * (0.00059 - Jcent * 0.001813)))) / 60) / 60
        obliq = Mobliq + 0.00256 * cos(rad(125.04 - 1934.136 * Jcent))
        vary = tan(rad(obliq / 2)) * tan(rad(obliq / 2))
        Seqcent = sin(rad(Manom)) * (1.914602 - Jcent * (0.004817 + 0.000014 * Jcent)) + sin(rad(2 * Manom)) * (0.019993 - 0.000101 * Jcent) + sin(rad(3 * Manom)) * 0.000289
        Struelong = Mlong + Seqcent
        Sapplong = Struelong - 0.00569 - 0.00478 * sin(rad(125.04 - 1934.136 * Jcent))
        declination = deg(asin(sin(rad(obliq)) * sin(rad(Sapplong))))
        
        eqtime = 4 * deg(vary * sin(2 * rad(Mlong)) - 2 * Eccent * sin(rad(Manom)) + 4 * Eccent * vary * sin(rad(Manom)) * cos(2 * rad(Mlong)) - 0.5 * vary * vary * sin(4 * rad(Mlong)) - 1.25 * Eccent * Eccent * sin(2 * rad(Manom)))
        
        hourangle = deg(acos(cos(rad(90.833)) / (cos(rad(latitude)) * cos(rad(declination))) - tan(rad(latitude)) * tan(rad(declination))))
        
        self.solarnoon_t = (720 - 4 * longitude - eqtime + timezone * 60) / 1440
        self.sunrise_t = self.solarnoon_t - hourangle * 4 / 1440
        self.sunset_t = self.solarnoon_t + hourangle * 4 / 1440