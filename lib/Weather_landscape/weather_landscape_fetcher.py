import json
import datetime
import requests
import pytz

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
        # 使用pytz处理时区
        self.local_tz = pytz.timezone('Asia/Shanghai')  # 默认使用中国时区，可以根据需要修改
        self.tzoffset = datetime.datetime.now(self.local_tz).utcoffset().total_seconds()/(60*60)
        
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
        
        # 使用pytz将UTC时间转换为本地时间
        utc_time = datetime.datetime.utcfromtimestamp(int(data['dt']))
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(self.local_tz)
        
        weather_info = {
            'time': local_time,
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

        # Ensure max_time is offset-aware
        if max_time.tzinfo is None or max_time.tzinfo.utcoffset(max_time) is None:
            max_time = self.local_tz.localize(max_time)

        tmax = -999
        tmin = 999
        is_first = True

        for weather in self.weather_data:
            if is_first:
                is_first = False
                continue

            if weather['time'] > max_time:
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
        # Ensure time is offset-aware
        if time.tzinfo is None or time.tzinfo.utcoffset(time) is None:
            time = self.local_tz.localize(time)

        for weather in self.weather_data:
            if weather['time'] > time:
                return weather
        return None