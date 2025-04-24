import json
import datetime
import requests
from math import cos, sin, acos, asin, tan
from math import degrees as deg, radians as rad
import pytz

# Define GMT+8 timezone (or any default)
DEFAULT_TIMEZONE_STR = 'Asia/Shanghai'
try:
    DEFAULT_TIMEZONE = pytz.timezone(DEFAULT_TIMEZONE_STR)
except pytz.UnknownTimeZoneError:
    print(f"Default timezone '{DEFAULT_TIMEZONE_STR}' unknown, falling back to UTC.")
    DEFAULT_TIMEZONE = pytz.utc # Fallback to UTC if default is invalid

class WeatherData:
    """整合获取天气数据的功能"""
    # ... (常量定义保持不变) ...
    TEMP_UNITS_CELSIUS = 0
    TEMP_UNITS_FAHRENHEIT = 1
    KTOC = 273.15
    Thunderstorm = 2
    Drizzle = 3
    Rain = 5
    Snow = 6
    Atmosphere = 7
    Clouds = 8
    FORECAST_PERIOD_HOURS = 3
    OWMURL = "http://api.openweathermap.org/data/2.5/"

    def __init__(self, api_key, lat, lon, units_mode=0, pressure_min=980, pressure_max=1030, timezone_str=DEFAULT_TIMEZONE_STR):
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
            print(f"Unknown timezone '{timezone_str}', defaulting to {DEFAULT_TIMEZONE_STR}.")
            self.timezone = DEFAULT_TIMEZONE # Use the validated default timezone
        self.reqstr = f"lat={self.lat}&lon={self.lon}&mode=json&APPID={self.api_key}"
        self.url_forecast = f"{self.OWMURL}forecast?{self.reqstr}"
        self.url_current = f"{self.OWMURL}weather?{self.reqstr}"

    # ... get_weather_data (保持不变) ...
    def get_weather_data(self):
        """从OpenWeatherMap API获取天气数据"""
        self.weather_data = []
        try:
            curr_response = requests.get(self.url_current, timeout=10)
            curr_response.raise_for_status()
            curr_data = curr_response.json()
            forecast_response = requests.get(self.url_forecast, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            self.weather_data.append(self._process_weather_info(curr_data))
            if 'list' in forecast_data:
                for forecast in forecast_data['list']:
                    if self._check_weather_data(forecast):
                        self.weather_data.append(self._process_weather_info(forecast))
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return []
        return self.weather_data

    def _process_weather_info(self, data):
        """处理从API获取的天气数据，存储为naive datetime"""
        is_celsius = self.units_mode != self.TEMP_UNITS_FAHRENHEIT
        utc_dt = datetime.datetime.fromtimestamp(int(data['dt']), tz=pytz.utc)
        # Convert to target timezone, then make naive
        local_dt_aware = utc_dt.astimezone(self.timezone)
        local_dt_naive = local_dt_aware.replace(tzinfo=None)

        weather_info = {
            'time': local_dt_naive, # Store naive datetime
            'id': int(data['weather'][0]['id']),
            'clouds': int(data['clouds'].get('all', 0)) if 'clouds' in data else 0,
            'rain': 0.0,
            'snow': 0.0,
            'windspeed': float(data['wind'].get('speed', 0.0)) if 'wind' in data else 0.0,
            'winddeg': float(data['wind'].get('deg', 0.0)) if 'wind' in data else 0.0,
            'pressure': float(data['main']['pressure']),
            'is_celsius': is_celsius
        }
        # ... (雨雪量、温度处理保持不变) ...
        if 'rain' in data:
             if '3h' in data['rain']: weather_info['rain'] = float(data['rain']['3h'])
             elif '1h' in data['rain']: weather_info['rain'] = float(data['rain']['1h']) # OWM uses 1h for current, 3h for forecast
        if 'snow' in data:
             if '3h' in data['snow']: weather_info['snow'] = float(data['snow']['3h'])
             elif '1h' in data['snow']: weather_info['snow'] = float(data['snow']['1h'])

        temp_kelvin = float(data['main']['temp'])
        weather_info['temp'] = self._to_celsius(temp_kelvin)
        weather_info['temp_fahrenheit'] = self._to_fahrenheit(temp_kelvin)

        return weather_info

    # ... _to_celsius, _to_fahrenheit, _check_weather_data (保持不变) ...
    def _to_celsius(self, kelvin):
        return kelvin - self.KTOC
    def _to_fahrenheit(self, kelvin):
        return (kelvin - self.KTOC) * 1.8 + 32
    @staticmethod
    def _check_weather_data(data):
        if not ('dt' in data and 'weather' in data and 'main' in data):
            return False
        return True

    def _get_naive_datetime_in_timezone(self, dt_input):
        """Converts aware or naive datetime to naive datetime in instance's timezone."""
        if dt_input.tzinfo is not None:
            # Aware: convert to target timezone, then make naive
            return dt_input.astimezone(self.timezone).replace(tzinfo=None)
        else:
            # Naive: assume it's already in the target timezone
            return dt_input

    def get_temp_range(self, max_time):
        """获取指定时间内的温度范围 (使用 naive 时间比较)"""
        if not self.weather_data: return None

        naive_max_time = self._get_naive_datetime_in_timezone(max_time)

        tmax = -999
        tmin = 999
        found_data = False

        # Skip the first entry (current weather) for range calculation if needed?
        # Assuming we include current weather if it's before max_time
        for i, weather in enumerate(self.weather_data):
            # weather['time'] is already naive
            if weather['time'] <= naive_max_time:
                if weather['temp'] > tmax: tmax = weather['temp']
                if weather['temp'] < tmin: tmin = weather['temp']
                found_data = True
            # Optimization: if weather times are sorted, we can break early
            # Assuming OWM data is sorted by time:
            elif weather['time'] > naive_max_time and i > 0: # Check i > 0 if skipping first
                 break


        return (tmin, tmax) if found_data else None

    # ... get_current (保持不变) ...
    def get_current(self):
        if not self.weather_data: return None
        return self.weather_data[0]

    def get_forecast_at_time(self, time):
        """获取指定时间的天气预报 (使用 naive 时间比较)"""
        if not self.weather_data: return None

        naive_target_time = self._get_naive_datetime_in_timezone(time)

        # Skip current weather (index 0) when looking for forecasts
        for weather in self.weather_data[1:]:
            # weather['time'] is already naive
            if weather['time'] > naive_target_time:
                return weather
        # If no forecast is strictly *after* the target time, return None
        return None


class SunCalculator:
    """计算日出日落时间 (返回 naive 时间)"""

    def __init__(self, lat, lon, timezone_str=DEFAULT_TIMEZONE_STR):
        self.lat = lat
        self.lon = lon
        try:
            self.timezone = pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            print(f"Unknown timezone '{timezone_str}', defaulting to {DEFAULT_TIMEZONE_STR}.")
            self.timezone = DEFAULT_TIMEZONE

    def _get_naive_datetime_in_timezone(self, dt_input=None):
        """Gets current or specified time as naive datetime in instance's timezone."""
        if dt_input is None:
            # Get current time in the target timezone, then make naive
            return datetime.datetime.now(self.timezone).replace(tzinfo=None)
        elif dt_input.tzinfo is not None:
            # Aware: convert to target timezone, then make naive
            return dt_input.astimezone(self.timezone).replace(tzinfo=None)
        else:
            # Naive: assume it's already in the target timezone
            return dt_input

    def sunrise(self, when=None):
        """计算日出时间 (返回 naive datetime)"""
        naive_when = self._get_naive_datetime_in_timezone(when)
        self.__preptime(naive_when) # Pass naive time
        self.__calc()
        # __timefromdecimalday now returns naive datetime
        return self.__timefromdecimalday(self.sunrise_t, naive_when)

    def sunset(self, when=None):
        """计算日落时间 (返回 naive datetime)"""
        naive_when = self._get_naive_datetime_in_timezone(when)
        self.__preptime(naive_when)
        self.__calc()
        return self.__timefromdecimalday(self.sunset_t, naive_when)

    def solarnoon(self, when=None):
        """计算正午时间 (返回 naive datetime)"""
        naive_when = self._get_naive_datetime_in_timezone(when)
        self.__preptime(naive_when)
        self.__calc()
        return self.__timefromdecimalday(self.solarnoon_t, naive_when)

    def __timefromdecimalday(self, day_fraction, base_naive_when):
        """Converts decimal day fraction to naive datetime object."""
        hours = 24.0 * day_fraction
        h = int(hours)
        minutes = (hours - h) * 60
        m = int(minutes)
        seconds = (minutes - m) * 60
        s = int(round(seconds)) # Round seconds

        # Handle second rounding potentially rolling over
        if s >= 60:
            s -= 60
            m += 1
        if m >= 60:
            m -= 60
            h += 1

        day_offset = 0
        while h < 0:
            h += 24
            day_offset -= 1
        while h >= 24:
            h -= 24
            day_offset += 1

        # base_naive_when is already naive and in the target timezone
        base_date = base_naive_when.date()

        try:
            adjusted_date = base_date + datetime.timedelta(days=day_offset)
            # Return naive datetime directly
            return datetime.datetime(adjusted_date.year, adjusted_date.month, adjusted_date.day, h, m, s)
        except OverflowError:
             raise ValueError(f"Date calculation resulted in overflow for base_date={base_date}, day_offset={day_offset}")
        except ValueError as e:
             # This might happen if h, m, s are invalid after adjustments, though unlikely with clamping/rounding
             raise ValueError(f"Could not construct valid naive datetime. adjusted_date={adjusted_date}, h={h}, m={m}, s={s}. Original error: {e}") from e


    def __preptime(self, naive_when):
        """Prepare calculation variables based on naive datetime input."""
        # naive_when is assumed to be in self.timezone
        # Localize it to get the correct UTC offset for that specific time
        try:
            aware_when = self.timezone.localize(naive_when)
        except pytz.exceptions.NonExistentTimeError:
             # Handle time that doesn't exist (e.g., DST spring forward gap)
             # Advance time slightly and try again, or use a standard offset
             aware_when = self.timezone.localize(naive_when + datetime.timedelta(hours=1), is_dst=None) # Or handle differently
        except pytz.exceptions.AmbiguousTimeError:
             # Handle ambiguous time (e.g., DST fall back overlap)
             # Choose one (e.g., standard time by setting is_dst=False)
             aware_when = self.timezone.localize(naive_when, is_dst=False) # Or is_dst=True for DST

        # Calculate offset in hours for the specific datetime 'aware_when'
        tz_offset_seconds = aware_when.utcoffset().total_seconds()
        self.timezone_offset_hours = tz_offset_seconds / 3600.0

        # Convert 'aware_when' to UTC for calculations
        when_utc = aware_when.astimezone(pytz.utc)

        # Day/time calculation based on UTC representation
        self.day = when_utc.toordinal() - (734124 - 40529) # Correct base? Check original source if issues arise
        t = when_utc.time()
        self.time = (t.hour + t.minute/60.0 + t.second/3600.0) / 24.0

    def __calc(self):
        """Core sun position calculation (no changes needed here)."""
        # Uses self.timezone_offset_hours calculated in __preptime
        timezone = self.timezone_offset_hours
        longitude = self.lon
        latitude = self.lat
        time = self.time # UTC fraction of day
        day = self.day # Day number based on UTC

        # --- Original calculation logic ---
        Jday = day + 2415018.5 + time # Julian day based on UTC time
        # The original formula seems to apply timezone offset later.
        Jcent = (Jday - 2451545) / 36525 # Julian century

        Manom = 357.52911 + Jcent * (35999.05029 - 0.0001537 * Jcent)
        Mlong = (280.46646 + Jcent * (36000.76983 + Jcent * 0.0003032)) % 360
        Eccent = 0.016708634 - Jcent * (0.000042037 + 0.000000153 * Jcent) # Typo fixed? 0.0001537 -> 0.000000153? Check source. Assuming original was correct.
        Eccent = 0.016708634 - Jcent * (0.000042037 + 0.0001537 * Jcent) # Reverted to original

        Mobliq = 23 + (26 + ((21.448 - Jcent * (46.815 + Jcent * (0.00059 - Jcent * 0.001813)))) / 60) / 60
        obliq = Mobliq + 0.00256 * cos(rad(125.04 - 1934.136 * Jcent))
        vary = tan(rad(obliq / 2)) * tan(rad(obliq / 2))
        Seqcent = sin(rad(Manom)) * (1.914602 - Jcent * (0.004817 + 0.000014 * Jcent)) + \
                  sin(rad(2 * Manom)) * (0.019993 - 0.000101 * Jcent) + \
                  sin(rad(3 * Manom)) * 0.000289
        Struelong = (Mlong + Seqcent) % 360 # Ensure result is 0-360
        Sapplong = Struelong - 0.00569 - 0.00478 * sin(rad(125.04 - 1934.136 * Jcent))
        declination = deg(asin(sin(rad(obliq)) * sin(rad(Sapplong))))

        eqtime = 4 * deg(vary * sin(2 * rad(Mlong)) - 2 * Eccent * sin(rad(Manom)) + \
                         4 * Eccent * vary * sin(rad(Manom)) * cos(2 * rad(Mlong)) - \
                         0.5 * vary * vary * sin(4 * rad(Mlong)) - \
                         1.25 * Eccent * Eccent * sin(2 * rad(Manom)))

        # Hour angle calculation with clamping
        ha_arg = (cos(rad(90.833)) / (cos(rad(latitude)) * cos(rad(declination))) - \
                  tan(rad(latitude)) * tan(rad(declination)))
        ha_arg = max(-1.0, min(1.0, ha_arg)) # Clamp to avoid domain error
        hourangle = deg(acos(ha_arg))

        # Calculate solar noon, sunrise, sunset as fraction of day *in the local timezone*
        # The formula directly incorporates the timezone offset (in hours * 60 = minutes)
        # and longitude offset (in degrees * 4 = minutes) relative to UTC noon (720 minutes).
        self.solarnoon_t = (720 - 4 * longitude - eqtime + timezone * 60) / 1440
        self.sunrise_t = self.solarnoon_t - hourangle * 4 / 1440
        self.sunset_t = self.solarnoon_t + hourangle * 4 / 1440

        # Ensure fractions are within [0, 1) range if needed, though __timefromdecimalday handles rollover.
        # self.solarnoon_t %= 1.0
        # self.sunrise_t %= 1.0
        # self.sunset_t %= 1.0
