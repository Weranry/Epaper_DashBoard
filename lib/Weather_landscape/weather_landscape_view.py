import os
import random
import math
import datetime
from PIL import Image, ImageOps
from .weather_landscape_fetcher import WeatherData, SunCalculator

class Sprites:
    """处理精灵图片绘制"""
    
    DISABLED = -999999
    
    # 颜色定义
    Black = 0  # 黑色对应索引值0
    White = 1  # 白色对应索引值1
    Red = 2    # 红色对应索引值2
    
    # 精灵图片中的颜色索引
    BLACK = 0  # 精灵图片中黑色对应索引0
    WHITE = 1  # 精灵图片中白色对应索引1
    RED = 2    # 精灵图片中红色对应索引2
    TRANS = 3  # 透明色
    
    PLASSPRITE = 10
    MINUSSPRITE = 11
    
    # 精灵文件扩展名
    EXT = ".png"
    
    def __init__(self, sprites_dir, canvas):
        self.img = canvas
        self.pix = self.img.load()
        self.dir = sprites_dir
        self.ext = self.EXT
        self.w, self.h = self.img.size
    
    def Dot(self, x, y, color):
        """绘制单个点"""
        if (y >= self.h) or (x >= self.w) or (y < 0) or (x < 0):
            return
        
        self.pix[x, y] = color
    
    def Draw(self, name, index, xpos, ypos, ismirror=False):
        """绘制精灵图像"""
        if (xpos < 0) or (ypos < 0):
            return 0
        
        imagefilename = "%s_%02i%s" % (name, index, self.ext)
        imagepath = os.path.join(self.dir, imagefilename)
        img = Image.open(imagepath)
        
        if ismirror:
            img = ImageOps.mirror(img)
            
        w, h = img.size
        pix = img.load()
        ypos -= h
        
        for x in range(w):
            for y in range(h):
                if (xpos + x >= self.w) or (xpos + x < 0):
                    continue
                if (ypos + y >= self.h) or (ypos + y < 0):
                    continue
                    
                if pix[x, y] == self.BLACK:
                    self.Dot(xpos + x, ypos + y, self.Black)
                elif pix[x, y] == self.WHITE:
                    self.Dot(xpos + x, ypos + y, self.White)
                elif pix[x, y] == self.RED:
                    self.Dot(xpos + x, ypos + y, self.Red)
        
        return w
    
    # 数字精灵常量
    DIGITPLAS = 10
    DIGITMINUS = 11
    DIGITSEMICOLON = 12
    
    def DrawInt(self, n, xpos, ypos, issign=True, mindigits=1):
        """绘制整数"""
        n = round(n)
        if n < 0:
            sign = self.DIGITMINUS
        else:
            sign = self.DIGITPLAS
            
        n = abs(n)
        n0 = int(n / 100)
        n1 = int((n % 100) / 10)
        n2 = n % 10
        dx = 0
        
        if (issign) or (sign == self.DIGITMINUS):
            w = self.Draw("digit", sign, xpos + dx, ypos)
            dx += w + 1
            
        if (n0 != 0) or (mindigits >= 3):
            w = self.Draw("digit", n0, xpos + dx, ypos)
            dx += w
            if (n0 != 1):
                dx += 1
                
        if (n1 != 0) or (n0 != 0) or (mindigits >= 2):
            if (n1 == 1):
                dx -= 1
            w = self.Draw("digit", n1, xpos + dx, ypos)
            dx += w
            if (n1 != 1):
                dx += 1
                
        if (n2 == 1):
            dx -= 1
        w = self.Draw("digit", n2, xpos + dx, ypos)
        dx += w
        if (n2 != 1):
            dx += 1
            
        return dx
    
    def DrawClock(self, xpos, ypos, h, m):
        """绘制时钟"""
        dx = 0
        w = self.DrawInt(h, xpos + dx, ypos, False, 2)
        dx += w
        w = self.Draw("digit", self.DIGITSEMICOLON, xpos + dx, ypos)
        dx += w
        dx = self.DrawInt(m, xpos + dx, ypos, False, 2)
        dx += w + 1
        return dx
    
    # 云朵绘制相关常量
    CLOUDWMAX = 32
    CLOUDS = [2, 3, 5, 10, 30, 50]
    CLOUDK = 0.5
    
    def DrawCloud(self, persent, xpos, ypos, width, height):
        """绘制云朵"""
        if persent < 2:
            return
        elif persent < 5:
            cloudset = [2]
        elif persent < 10:
            cloudset = [3, 2]
        elif persent < 20:
            cloudset = [5, 3, 2]
        elif persent < 30:
            cloudset = [10, 5]
        elif persent < 40:
            cloudset = [10, 10]
        elif persent < 50:
            cloudset = [10, 10, 5]
        elif persent < 60:
            cloudset = [30, 5]
        elif persent < 70:
            cloudset = [30, 10]
        elif persent < 80:
            cloudset = [30, 10, 5, 5]
        elif persent < 90:
            cloudset = [30, 10, 10]
        else:
            cloudset = [50, 30, 10, 10, 5]
        
        dx = width
        for c in cloudset:
            self.Draw("cloud", c, xpos + random.randrange(dx), ypos)
    
    # 雨水绘制相关常量
    HEAVYRAIN = 5.0
    RAINFACTOR = 20
    
    def DrawRain(self, value, xpos, ypos, width, tline):
        """绘制雨水"""
        ypos += 1
        r = 1.0 - (value / self.HEAVYRAIN) / self.RAINFACTOR
        
        for x in range(xpos, xpos + width):
            for y in range(ypos, tline[x], 2):
                if (x >= self.w):
                    continue
                if (y >= self.h):
                    continue
                if (random.random() > r):
                    self.pix[x, y] = self.Black
                    self.pix[x, y - 1] = self.Black
    
    # 雪花绘制相关常量
    HEAVYSNOW = 5.0
    SNOWFACTOR = 10
    
    def DrawSnow(self, value, xpos, ypos, width, tline):
        """绘制雪花"""
        ypos += 1
        r = 1.0 - (value / self.HEAVYSNOW) / self.SNOWFACTOR
        
        for x in range(xpos, xpos + width):
            for y in range(ypos, tline[x], 2):
                if (x >= self.w):
                    continue
                if (y >= self.h):
                    continue
                if (random.random() > r):
                    self.pix[x, y] = self.Black
    
    def DrawWind_degdist(self, deg1, deg2):
        """计算角度距离"""
        h = max(deg1, deg2)
        l = min(deg1, deg2)
        d = h - l
        if d > 180:
            d = 360 - d
        return d
    
    def DrawWind_dirsprite(self, dir, dir0, name, list):
        """添加风向相关精灵"""
        count = [4, 3, 3, 2, 2, 1, 1]
        step = 11.25  # degrees
        dist = self.DrawWind_degdist(dir, dir0)
        n = int(dist / step)
        if n < len(count):
            for i in range(0, count[n]):
                list.append(name)
    
    def DrawWind(self, speed, direction, xpos, tline):
        """绘制风向"""
        list = []
        
        self.DrawWind_dirsprite(direction, 0, "pine", list)
        self.DrawWind_dirsprite(direction, 90, "east", list)
        self.DrawWind_dirsprite(direction, 180, "palm", list)
        self.DrawWind_dirsprite(direction, 270, "tree", list)
        
        random.shuffle(list)
        
        windindex = None
        if speed <= 0.4:
            windindex = []
        elif speed <= 0.7:
            windindex = [0]
        elif speed <= 1.7:
            windindex = [1, 0, 0]
        elif speed <= 3.3:
            windindex = [1, 1, 0, 0]
        elif speed <= 5.2:
            windindex = [1, 2, 0, 0]
        elif speed <= 7.4:
            windindex = [1, 2, 2, 0]
        elif speed <= 9.8:
            windindex = [1, 2, 3, 0]
        elif speed <= 12.4:
            windindex = [2, 2, 3, 0]
        else:
            windindex = [3, 3, 3, 3]
        
        if windindex is not None:
            ix = int(xpos)
            random.shuffle(windindex)
            j = 0
            
            for i in windindex:
                if j >= len(list):
                    break
                    
                xx = ix + random.randint(-1, 1)
                ismirror = random.random() < 0.5
                offset = xx + 5
                
                if offset >= len(tline):
                    break
                
                if ismirror:
                    xx -= 16
                
                self.Draw(list[j], i, xx, tline[offset] + 1, ismirror)
                ix += 9
                j += 1
    
    # 烟雾绘制相关常量
    SMOKE_R_PX = 30
    PERSENT_DELTA = 4
    SMOKE_SIZE = 60
    
    def DrawSmoke_makeline(self, angle_deg):
        """生成烟雾线"""
        a = (math.pi * angle_deg) / 180
        r = self.SMOKE_R_PX
        k = r * math.sin(a) / (math.sqrt((r * math.cos(a))))
        yp = 0
        dots = []
        
        for x in range(0, self.w):
            y = int(k * math.sqrt(x))
            if y > self.h:
                y = self.h
            yi = yp
            
            while True:
                rr = math.sqrt(x * x + yi * yi)
                dots.append([x, yi, rr])
                if rr > self.SMOKE_SIZE:
                    return dots
                yi += 1
                if yi >= y:
                    yp = y
                    break
    
    def DrawSmoke(self, x0, y0, percent):
        """绘制烟雾"""
        dots = self.DrawSmoke_makeline(percent)
        for d in dots:
            x = d[0]
            y = d[1]
            r = d[2]
            if random.random() * 1.3 > (r / self.SMOKE_SIZE):
                if random.random() * 1.2 < (r / self.SMOKE_SIZE):
                    dx = random.randint(-1, 1)
                    dy = random.randint(-1, 1)
                else:
                    dx = 0
                    dy = 0
                
                self.Dot(x0 + x + dx, self.h - (y0 + y) + dy, self.Black)


class WeatherDrawer:
    # ... existing code ...

    def draw_weather(self, weather_data: WeatherData): # Add type hint
        """绘制天气图"""
        # ... (图像和精灵初始化) ...
        img = Image.new('P', (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), color=1)
        palette = [0, 0, 0, 255, 255, 255, 255, 0, 0] + [0, 0, 0] * 253
        img.putpalette(palette)
        sprite = Sprites(self.SPRITES_DIR, img)
        self.pic_height = self.IMAGE_HEIGHT
        self.pic_width = self.IMAGE_WIDTH
        self.ypos = self.DRAWOFFSET

        # --- Consistent Naive Time Handling ---
        # Use the current weather data's time as the reference "now"
        f_current = weather_data.get_current()
        if f_current is None or 'time' not in f_current:
            print("Error: No current weather data or time available. Cannot proceed.")
            # Fallback or return error image
            # As a fallback, we might try datetime.now(), but it leads back to the original problem.
            # Let's return a blank image for now.
            return img.convert('RGB')

        # This is the crucial change: Use data-derived time, not execution time.
        t_naive_now = f_current['time'] # Already naive and in target timezone
        # ---

        # ... (计算 n_forecast_periods) ...
        if self.XSTEP <= 0:
             print("Error: XSTEP must be positive.")
             return img.convert('RGB')
        n_forecast_periods = (self.pic_width - self.XSTART) / self.XSTEP

        # Calculate max_time based on data-derived naive current time
        max_time_naive = t_naive_now + datetime.timedelta(hours=WeatherData.FORECAST_PERIOD_HOURS * n_forecast_periods)

        # ... (获取温度范围 temp_range_result, 计算 degree_per_pixel) ...
        temp_range_result = weather_data.get_temp_range(max_time_naive)
        # ... (rest of temp range and degree_per_pixel calculation) ...

        # ... (初始化 tline, old_temp, old_y using f_current) ...
        initial_y = self.ypos + self.YSTEP // 2
        tline_size = self.pic_width + self.XSTEP * 2
        tline = [initial_y] * tline_size

        if 'temp' not in f_current:
             print("Error: Current weather data missing 'temp'. Using average.")
             old_temp = (self.tmin + self.tmax) / 2 if self.tmin is not None and self.tmax is not None else 10 # Default temp
        else:
             old_temp = f_current['temp']
        old_y = self.deg_to_pix(old_temp)
        # Validate initial old_y
        if old_y == Sprites.DISABLED or old_y >= self.pic_height or old_y < 0:
             print(f"Warning: Initial temperature y-position ({old_y}) is invalid. Clamping.")
             old_y = max(0, min(self.pic_height -1, old_y if old_y != Sprites.DISABLED else initial_y))
        for i in range(self.XSTART):
             if i < len(tline):
                 tline[i] = old_y

        # ... (绘制初始元素: 房屋、烟雾、温度、云雨雪 - 使用 f_current) ...
        y_clouds = int(self.ypos - self.YSTEP / 2)
        if f_current and 'pressure' in f_current and 'clouds' in f_current and 'rain' in f_current and 'snow' in f_current:
            # ... (drawing house, smoke, temp, cloud, rain, snow) ...
            pass # Assuming this part is correct
        else:
             print("Warning: Missing data in f_current, skipping initial drawing elements.")


        # --- Use Naive Time Consistently ---
        # t is now correctly initialized from data
        t = t_naive_now
        # tf also starts from the data-derived time
        tf = t_naive_now
        # ---

        # ... (dt, x0, xpos, n_forecast_periods_int, bezier setup) ...
        dt = datetime.timedelta(hours=WeatherData.FORECAST_PERIOD_HOURS)
        x0 = int(self.XSTART)
        xpos = x0
        n_forecast_periods_int = int(n_forecast_periods)
        if self.XSTEP <= self.XFLAT or self.XFLAT < 0:
             print(f"Error: Invalid XSTEP ({self.XSTEP}) or XFLAT ({self.XFLAT}).")
             return img.convert('RGB')
        n_bezier = int((self.XSTEP - self.XFLAT) / 2)
        n_flat = int(self.XFLAT)
        n_bezier2 = self.XSTEP - n_flat - n_bezier

        # --- Draw Temperature Line using Bezier (using data-derived tf) ---
        prev_mid_x = x0 - self.XSTEP / 2.0
        prev_mid_y = old_y
        for i in range(n_forecast_periods_int + 1):
            # Pass naive tf (derived from data 'now') to get_forecast_at_time
            f = weather_data.get_forecast_at_time(tf)
            # ... (rest of the temperature line drawing loop, using tf) ...
            if f is None or 'temp' not in f:
                new_temp = old_temp
                new_y = old_y
            else:
                new_temp = f['temp']
                new_y = self.deg_to_pix(new_temp)
            # Validate new_y
            if new_y == Sprites.DISABLED or new_y >= self.pic_height or new_y < 0:
                 new_y = max(0, min(self.pic_height -1, new_y if new_y != Sprites.DISABLED else old_y))

            mid_x_current = xpos + n_bezier + n_flat / 2.0
            mid_y_current = new_y
            start_curve_x = int(prev_mid_x)
            end_curve_x = int(mid_x_current)
            for current_x in range(start_curve_x, end_curve_x):
                 if 0 <= current_x < tline_size:
                      try:
                           tline[current_x] = self.my_bezier(current_x, prev_mid_x, prev_mid_y, mid_x_current, mid_y_current)
                      except ZeroDivisionError:
                           tline[current_x] = prev_mid_y
            flat_start_x = xpos + n_bezier
            flat_end_x = flat_start_x + n_flat
            for current_x in range(int(flat_start_x), int(flat_end_x)):
                 if 0 <= current_x < tline_size:
                      tline[current_x] = new_y

            old_temp = new_temp
            old_y = new_y
            prev_mid_x = mid_x_current
            prev_mid_y = mid_y_current
            xpos += self.XSTEP
            tf += dt # Increment naive forecast time iterator

        # ... (copy tline0, block initial range) ...
        tline0 = tline[:self.pic_width]
        self.block_range(tline, 0, x0 + 10)

        # --- Draw Sun/Moon/Markers (using data-derived tf) ---
        try:
             sun_calc = SunCalculator(weather_data.lat, weather_data.lon, weather_data.timezone.zone)
        except Exception as e:
             print(f"Error initializing SunCalculator: {e}. Sun/Moon markers might be inaccurate.")
             sun_calc = None

        # Reset tf to the data-derived 'now'
        tf = t_naive_now
        xpos = self.XSTART
        drawn_events = {}

        for i in range(n_forecast_periods_int + 2):
            if sun_calc is None: break
            tf_start = tf
            tf_end = tf + dt
            current_date = tf_start.date()
            if current_date not in drawn_events: drawn_events[current_date] = set()

            try:
                 # Pass naive tf_start (derived from data 'now')
                 t_sunrise_naive = sun_calc.sunrise(tf_start)
                 t_sunset_naive = sun_calc.sunset(tf_start)
            except ValueError as e:
                 print(f"Warning: Could not calculate sunrise/sunset for {current_date}: {e}")
                 t_sunrise_naive = None
                 t_sunset_naive = None

            t_noon_naive = datetime.datetime(current_date.year, current_date.month, current_date.day, 12, 0, 0)
            t_midn_naive = datetime.datetime(current_date.year, current_date.month, current_date.day) + datetime.timedelta(days=1)

            # get_pixel_offset uses tf_start which is now derived from data 'now'
            def get_pixel_offset(event_time_naive):
                 # ... (get_pixel_offset implementation remains the same) ...
                 if event_time_naive is None: return None
                 if event_time_naive.tzinfo is not None:
                      event_time_naive = event_time_naive.replace(tzinfo=None)
                 time_diff = event_time_naive - tf_start
                 if datetime.timedelta(0) <= time_diff < dt:
                      return self.time_diff_to_pixels(time_diff)
                 return None


            y_sun_moon = self.ypos - self.YSTEP * 5 // 8

            # ... (drawing sun, moon, noon, midnight markers using get_pixel_offset) ...
            # Sunrise
            if 'sunrise' not in drawn_events[current_date]:
                 offset = get_pixel_offset(t_sunrise_naive)
                 if offset is not None:
                      sprite.Draw("sun", 0, xpos + offset, y_sun_moon)
                      drawn_events[current_date].add('sunrise')
            # Sunset
            if 'sunset' not in drawn_events[current_date]:
                 offset = get_pixel_offset(t_sunset_naive)
                 if offset is not None:
                      sprite.Draw("moon", 0, xpos + offset, y_sun_moon)
                      drawn_events[current_date].add('sunset')
            # Noon
            if 'noon' not in drawn_events[current_date]:
                 offset = get_pixel_offset(t_noon_naive)
                 if offset is not None:
                      ix = int(xpos + offset)
                      if 0 <= ix < len(tline):
                           line_y = tline[ix]
                           if line_y != Sprites.DISABLED:
                                sprite.Draw("flower", 1, ix, line_y + 1)
                                self.block_range(tline, ix - self.FLOWER_LEFT_PX, ix + self.FLOWER_RIGHT_PX)
                                drawn_events[current_date].add('noon')
            # Midnight
            if 'midnight' not in drawn_events[current_date]:
                 offset = get_pixel_offset(t_midn_naive)
                 if offset is not None:
                      ix = int(xpos + offset)
                      if 0 <= ix < len(tline):
                           line_y = tline[ix]
                           if line_y != Sprites.DISABLED:
                                sprite.Draw("flower", 0, ix, line_y + 1)
                                self.block_range(tline, ix - self.FLOWER_LEFT_PX, ix + self.FLOWER_RIGHT_PX)
                                drawn_events[current_date].add('midnight')


            xpos += self.XSTEP
            tf += dt # Increment naive forecast time iterator

        # --- Draw Min/Max Temp & Details (using data-derived tf) ---
        # Reset tf to the data-derived 'now'
        tf = t_naive_now
        xpos = self.XSTART
        f_used_markers = set()
        min_temp_drawn = False
        max_temp_drawn = False

        for i in range(n_forecast_periods_int + 1):
            # Pass naive tf (derived from data 'now')
            f = weather_data.get_forecast_at_time(tf)
            # ... (rest of the min/max temp and details drawing loop, using tf) ...
            if f is None or 'temp' not in f or 'time' not in f: # Ensure 'time' exists
                 tf += dt
                 xpos += self.XSTEP
                 continue

            center_x = xpos + n_bezier + n_flat // 2
            line_y_at_center = tline0[center_x] if 0 <= center_x < len(tline0) else self.ypos

            current_temp = f['temp']
            is_min = abs(current_temp - self.tmin) < 0.01 if self.tmin is not None else False
            is_max = abs(current_temp - self.tmax) < 0.01 if self.tmax is not None else False

            if is_min and not min_temp_drawn and line_y_at_center != Sprites.DISABLED:
                 self.draw_temperature(f, center_x, line_y_at_center, sprite)
                 min_temp_drawn = True
            elif is_max and not max_temp_drawn and line_y_at_center != Sprites.DISABLED:
                 self.draw_temperature(f, center_x, line_y_at_center, sprite)
                 max_temp_drawn = True

            forecast_time_key = f['time'] # Naive time as key
            if forecast_time_key not in f_used_markers:
                # Ensure necessary keys exist before drawing details
                if 'windspeed' in f and 'winddeg' in f and 'clouds' in f and 'rain' in f and 'snow' in f:
                    y_clouds = int(self.ypos - self.YSTEP / 2)
                    sprite.DrawWind(f['windspeed'], f['winddeg'], xpos, tline)
                    sprite.DrawCloud(f['clouds'], xpos, y_clouds, self.XSTEP, self.YSTEP / 2)
                    sprite.DrawRain(f['rain'], xpos, y_clouds, self.XSTEP, tline0)
                    sprite.DrawSnow(f['snow'], xpos, y_clouds, self.XSTEP, tline0)
                    f_used_markers.add(forecast_time_key)
                else:
                    print(f"Warning: Missing data in forecast for {forecast_time_key}, skipping details drawing.")


            xpos += self.XSTEP
            tf += dt

        # ... (Final pass to draw temperature line) ...
        for x in range(self.pic_width):
            y = tline0[x]
            if y != Sprites.DISABLED and 0 <= y < self.pic_height:
                sprite.Dot(x, y, Sprites.Black)

        # ... (Convert to RGB and return) ...
        img_rgb = img.convert('RGB')
        return img_rgb