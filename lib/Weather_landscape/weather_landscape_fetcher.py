import json
import datetime
import requests
from math import cos, sin, acos, asin, tan
from math import degrees as deg, radians as rad
import pytz  # Import pytz

# Define GMT+8 timezone
GMT8 = pytz.timezone('Asia/Shanghai')

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
    
    def __init__(self, api_key, lat, lon, units_mode=0, pressure_min=980, pressure_max=1030, timezone_str='Asia/Shanghai'):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.units_mode = units_mode
        self.pressure_min = pressure_min
        self.pressure_max = pressure_max
        self.weather_data = []
        try:
            self.timezone = pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            print(f"Unknown timezone '{timezone_str}', defaulting to GMT+8.")
            self.timezone = GMT8 # Default to GMT+8 if provided timezone is invalid
        
        # 构建API请求URL
        self.reqstr = f"lat={self.lat}&lon={self.lon}&mode=json&APPID={self.api_key}"
        self.url_forecast = f"{self.OWMURL}forecast?{self.reqstr}"
        self.url_current = f"{self.OWMURL}weather?{self.reqstr}"
    
    def get_weather_data(self):
        """从OpenWeatherMap API获取天气数据"""
        self.weather_data = []
        
        try:
            # 使用requests库获取当前天气，设置超时时间为10秒
            curr_response = requests.get(self.url_current, timeout=10)
            curr_response.raise_for_status() # 检查请求是否成功
            curr_data = curr_response.json()
            
            # 使用requests库获取天气预报，设置超时时间为10秒
            forecast_response = requests.get(self.url_forecast, timeout=10)
            forecast_response.raise_for_status() # 检查请求是否成功
            forecast_data = forecast_response.json()
            
            # 处理当前天气数据
            self.weather_data.append(self._process_weather_info(curr_data))
            
            # 处理预报数据
            if 'list' in forecast_data:
                for forecast in forecast_data['list']:
                    if self._check_weather_data(forecast):
                        self.weather_data.append(self._process_weather_info(forecast))
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}") # 打印错误信息
            # 可以选择返回空列表或抛出异常，这里返回空列表
            return [] 
            
        return self.weather_data
    
    def _process_weather_info(self, data):
        """处理从API获取的天气数据"""
        is_celsius = self.units_mode != self.TEMP_UNITS_FAHRENHEIT
        
        # Convert UTC timestamp to the specified timezone
        utc_dt = datetime.datetime.fromtimestamp(int(data['dt']), tz=pytz.utc)
        local_dt = utc_dt.astimezone(self.timezone)

        weather_info = {
            'time': local_dt, # Use timezone-aware datetime
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
    
    def get_temp_range(self, max_time):
        """获取指定时间内的温度范围"""
        if len(self.weather_data) == 0:
            return None
            
        # Ensure max_time is timezone-aware and matches self.timezone
        if max_time.tzinfo is None:
            # Assume naive max_time is in the instance's timezone
            aware_max_time = self.timezone.localize(max_time)
        else:
            # Convert max_time to the instance's timezone if different
            aware_max_time = max_time.astimezone(self.timezone)
            
        tmax = -999
        tmin = 999
        is_first = True
        
        for weather in self.weather_data:
            # weather['time'] is already aware and in self.timezone
            if is_first:
                is_first = False
                continue
                
            # Compare aware datetimes
            if weather['time'] > aware_max_time:
                break
                
            if weather['temp'] > tmax:
                tmax = weather['temp']
                
            if weather['temp'] < tmin:
                tmin = weather['temp']
                
        # Return None if no data points were within the time range (excluding the first)
        if tmax == -999 and tmin == 999 and len(self.weather_data) > 1:
             return None
        elif tmax == -999 and tmin == 999: # Handle case with only current weather
             return None

        return (tmin, tmax)
    
    def get_current(self):
        """获取当前天气数据"""
        if len(self.weather_data) == 0:
            return None
        return self.weather_data[0]
    
    def get_forecast_at_time(self, time):
        """获取指定时间的天气预报"""
        # Ensure time is timezone-aware and matches self.timezone
        if time.tzinfo is None:
            # Assume naive time is in the instance's timezone
            aware_time = self.timezone.localize(time)
        else:
            # Convert time to the instance's timezone if different
            aware_time = time.astimezone(self.timezone)
            
        for weather in self.weather_data:
            # weather['time'] is already aware and in self.timezone
            # Compare aware datetimes
            if weather['time'] > aware_time:
                return weather
        # If no forecast is later than the requested time, return the last available one?
        # Or return None if strictly looking for forecast *after* the time.
        # Current behavior: returns None if loop completes.
        return None


class SunCalculator:
    """计算日出日落时间"""
    
    def __init__(self, lat, lon, timezone_str='Asia/Shanghai'):
        self.lat = lat
        self.lon = lon
        try:
            self.timezone = pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            print(f"Unknown timezone '{timezone_str}', defaulting to GMT+8.")
            self.timezone = GMT8 # Default to GMT+8

    def sunrise(self, when=None):
        """计算日出时间"""
        if when is None:
            when = datetime.datetime.now(self.timezone) # Use timezone-aware now
        self.__preptime(when)
        self.__calc()
        return self.__timefromdecimalday(self.sunrise_t, when)
    
    def sunset(self, when=None):
        """计算日落时间"""
        if when is None:
            when = datetime.datetime.now(self.timezone) # Use timezone-aware now
        self.__preptime(when)
        self.__calc()
        return self.__timefromdecimalday(self.sunset_t, when)
    
    def solarnoon(self, when=None):
        """计算正午时间"""
        if when is None:
            when = datetime.datetime.now(self.timezone) # Use timezone-aware now
        self.__preptime(when)
        self.__calc()
        return self.__timefromdecimalday(self.solarnoon_t, when)
    
    def __timefromdecimalday(self, day, when):
        hours = 24.0 * day
        h = int(hours)
        minutes = (hours - h) * 60
        seconds = (minutes - int(minutes)) * 60

        day_offset = 0
        while h < 0:
            h += 24
            day_offset -= 1
        while h >= 24:
            h -= 24
            day_offset += 1

        # Use the date part of the original 'when' datetime, but ensure it's naive for timedelta calculation
        if when.tzinfo is not None:
             base_date = when.astimezone(self.timezone).date()
        else:
             # If 'when' is naive, assume it's in the target timezone already for date calculation
             base_date = when.date()

        try:
            adjusted_date = base_date + datetime.timedelta(days=day_offset)
        except OverflowError:
            raise ValueError(f"Date calculation resulted in overflow for base_date={base_date}, day_offset={day_offset}")

        m = max(0, min(59, int(round(minutes))))
        s = max(0, min(59, int(round(seconds))))

        try:
            # Create a naive datetime first
            naive_dt = datetime.datetime(adjusted_date.year, adjusted_date.month, adjusted_date.day, h, m, s)
            # Localize the naive datetime to the target timezone
            localized_dt = self.timezone.localize(naive_dt)
            return localized_dt
        except ValueError as e:
            raise ValueError(f"Could not construct valid datetime. adjusted_date={adjusted_date}, h={h}, m={m}, s={s}. Original error: {e}") from e
    
    def __preptime(self, when):
        # Ensure 'when' is timezone-aware and in the target timezone
        if when.tzinfo is None:
            # If naive, assume it's in the target timezone and make it aware
            when = self.timezone.localize(when)
        else:
            # If aware but different timezone, convert it
            when = when.astimezone(self.timezone)

        # Calculate offset in hours for the specific datetime 'when'
        tz_offset_seconds = when.utcoffset().total_seconds()
        self.timezone_offset_hours = tz_offset_seconds / 3600.0 # Use the specific offset for 'when'

        # Convert 'when' to UTC for calculations that might assume UTC base
        when_utc = when.astimezone(pytz.utc)

        # Original day/time calculation based on UTC representation
        self.day = when_utc.toordinal() - (734124 - 40529)
        t = when_utc.time()
        self.time = (t.hour + t.minute/60.0 + t.second/3600.0) / 24.0
    
    def __calc(self):
        # Use the specific timezone offset calculated in __preptime
        timezone = self.timezone_offset_hours # in hours, east is positive
        longitude = self.lon      # in decimal degrees, east is positive
        latitude = self.lat       # in decimal degrees, north is positive
        
        time = self.time  # percentage past midnight (UTC), i.e. noon is 0.5
        day = self.day    # daynumber 1=1/1/1900 (based on UTC)
        
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