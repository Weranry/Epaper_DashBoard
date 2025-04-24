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
        # 使用固定的时区
        self.timezone = pytz.timezone('Asia/Shanghai')
        # 计算时区偏移（小时）
        now = datetime.datetime.now(self.timezone)
        self.tzoffset = now.utcoffset().total_seconds() / 3600
        
        # 构建API请求URL
        self.reqstr = f"lat={self.lat}&lon={self.lon}&mode=json&APPID={self.api_key}"
        self.url_forecast = f"{self.OWMURL}forecast?{self.reqstr}"
        self.url_current = f"{self.OWMURL}weather?{self.reqstr}"
    
    def get_weather_data(self):
        """从OpenWeatherMap API获取天气数据"""
        self.weather_data = []
        
        try:
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
        except Exception as e:
            print(f"Error fetching weather data: {e}")
        
        return self.weather_data
    
    def _process_weather_info(self, data):
        """处理从API获取的天气数据"""
        is_celsius = self.units_mode != self.TEMP_UNITS_FAHRENHEIT
        
        try:
            # 创建时区感知的datetime对象
            weather_time = datetime.datetime.fromtimestamp(int(data['dt']), self.timezone)
            
            weather_info = {
                'time': weather_time,
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
        except Exception as e:
            print(f"Error processing weather info: {e}")
            # 返回一个带有默认值的字典
            return {
                'time': datetime.datetime.now(self.timezone),
                'id': 800,  # 晴天
                'clouds': 0,
                'rain': 0.0,
                'snow': 0.0,
                'windspeed': 0.0,
                'winddeg': 0.0,
                'pressure': 1013.0,  # 标准大气压
                'is_celsius': is_celsius,
                'temp': 20.0,  # 默认温度
                'temp_fahrenheit': 68.0
            }
    
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
        """确保datetime对象是时区感知的"""
        if dt is None:
            return datetime.datetime.now(self.timezone)
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            return self.timezone.localize(dt)
        return dt.astimezone(self.timezone)
    
    def get_temp_range(self, max_time):
        """获取指定时间内的温度范围"""
        try:
            # 确保 max_time 是时区感知的
            max_time = self.ensure_localized(max_time)
    
            tmax = -999
            tmin = 999
            is_first = True
    
            for weather in self.weather_data:
                if is_first:
                    is_first = False
                    continue
    
                # 确保 weather['time'] 是时区感知的
                weather_time = self.ensure_localized(weather['time'])
    
                # 比较时区感知的datetime
                if weather_time > max_time:
                    break
    
                if weather['temp'] > tmax:
                    tmax = weather['temp']
    
                if weather['temp'] < tmin:
                    tmin = weather['temp']
    
            return (tmin, tmax)
        except Exception as e:
            print(f"Error in get_temp_range: {e}")
            return (0, 30)  # 返回默认温度范围

    def get_current(self):
        """获取当前天气数据"""
        if len(self.weather_data) == 0:
            return None
        return self.weather_data[0]
    
    def get_forecast_at_time(self, time):
        """获取指定时间的天气预报"""
        try:
            # 确保 time 是时区感知的
            time = self.ensure_localized(time)
    
            for weather in self.weather_data:
                # 确保 weather['time'] 是时区感知的
                weather_time = self.ensure_localized(weather['time'])
                if weather_time > time:
                    return weather
            return None
        except Exception as e:
            print(f"Error in get_forecast_at_time: {e}")
            return self.get_current()  # 如果出错，返回当前天气


class SunCalculator:
    """计算日出日落时间"""
    
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        # 使用固定的时区
        self.timezone = pytz.timezone('Asia/Shanghai')
        # 计算时区偏移（小时）
        now = datetime.datetime.now(self.timezone)
        self.tzoffset = now.utcoffset().total_seconds() / 3600
    
    def sunrise(self, when=None):
        """计算日出时间"""
        try:
            if when is None:
                when = datetime.datetime.now(self.timezone)
            else:
                when = self.ensure_localized(when)
            self.__preptime(when)
            self.__calc()
            return self.__timefromdecimalday(self.sunrise_t, when)
        except Exception as e:
            print(f"Error calculating sunrise: {e}")
            # 返回默认日出时间（早上6点）
            today = datetime.datetime.now(self.timezone).replace(hour=6, minute=0, second=0, microsecond=0)
            return today
    
    def sunset(self, when=None):
        """计算日落时间"""
        try:
            if when is None:
                when = datetime.datetime.now(self.timezone)
            else:
                when = self.ensure_localized(when)
            self.__preptime(when)
            self.__calc()
            return self.__timefromdecimalday(self.sunset_t, when)
        except Exception as e:
            print(f"Error calculating sunset: {e}")
            # 返回默认日落时间（晚上6点）
            today = datetime.datetime.now(self.timezone).replace(hour=18, minute=0, second=0, microsecond=0)
            return today
    
    def solarnoon(self, when=None):
        """计算正午时间"""
        try:
            if when is None:
                when = datetime.datetime.now(self.timezone)
            else:
                when = self.ensure_localized(when)
            self.__preptime(when)
            self.__calc()
            return self.__timefromdecimalday(self.solarnoon_t, when)
        except Exception as e:
            print(f"Error calculating solarnoon: {e}")
            # 返回默认正午时间（中午12点）
            today = datetime.datetime.now(self.timezone).replace(hour=12, minute=0, second=0, microsecond=0)
            return today
    
    def ensure_localized(self, dt):
        """确保datetime对象是时区感知的"""
        if dt is None:
            return datetime.datetime.now(self.timezone)
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            return self.timezone.localize(dt)
        return dt.astimezone(self.timezone)
    
    def __timefromdecimalday(self, day, when):
        """将小数表示的一天转换为datetime对象"""
        try:
            hours = 24.0 * day
            h = int(hours) % 24  # 确保小时在 0 到 23 范围内
            minutes = (hours - h) * 60
            m = int(minutes) % 60  # 确保分钟在 0 到 59 范围内
            seconds = (minutes - m) * 60
            s = int(seconds) % 60  # 确保秒在 0 到 59 范围内
            
            # 确保when是时区感知的
            when = self.ensure_localized(when)
            
            # 创建新的datetime对象
            when_date = when.date()
            
            # 如果计算出的时间可能是第二天的，调整日期
            if h < when.hour and h < 12:  # 如果计算出的小时比当前小时小，且是上午，可能是第二天
                when_date = when_date + datetime.timedelta(days=1)
            
            # 创建naive datetime
            naive_dt = datetime.datetime(when_date.year, when_date.month, when_date.day, h, m, s)
            # 添加时区信息
            return self.timezone.localize(naive_dt)
        except Exception as e:
            print(f"Error in __timefromdecimalday: {e}")
            # 返回当前时间作为后备
            return datetime.datetime.now(self.timezone)
    
    def __preptime(self, when):
        try:
            # 确保when是时区感知的
            when = self.ensure_localized(when)
            self.day = when.toordinal() - (734124 - 40529)
            t = when.time()
            self.time = (t.hour + t.minute/60.0 + t.second/3600.0) / 24.0
            self.timezone_hours = self.tzoffset
        except Exception as e:
            print(f"Error in __preptime: {e}")
            # 设置默认值
            self.day = datetime.datetime.now(self.timezone).toordinal() - (734124 - 40529)
            self.time = 0.5  # 中午
            self.timezone_hours = 8  # 假设东八区
    
    def __calc(self):
        try:
            timezone = self.timezone_hours  # in hours, east is positive
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
        except Exception as e:
            print(f"Error in __calc: {e}")
            # 设置默认值
            self.solarnoon_t = 0.5  # 中午12点
            self.sunrise_t = 0.25   # 早上6点
            self.sunset_t = 0.75    # 晚上6点