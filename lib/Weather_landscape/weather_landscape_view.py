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
    """天气绘图器"""
    
    # 绘图常量
    XSTART = 32
    XSTEP = 44
    XFLAT = 10
    YSTEP = 50
    DEFAULT_DEGREE_PER_PIXEL = 0.5
    FLOWER_RIGHT_PX = 15
    FLOWER_LEFT_PX = 10
    DRAWOFFSET = 235  # 修改为在图片下方绘制
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 300
    
    # 使用绝对路径并确保sprite文件夹存在
    @staticmethod
    def ensure_sprites_dir():
        sprites_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprite")
        # 验证目录是否存在
        if not os.path.exists(sprites_dir):
            print(f"警告: 精灵图片目录不存在: {sprites_dir}")
            # 尝试查找其他可能的路径
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            alt_sprites_dir = os.path.join(parent_dir, "lib", "Weather_landscape", "sprite")
            if os.path.exists(alt_sprites_dir):
                print(f"使用替代路径: {alt_sprites_dir}")
                return alt_sprites_dir
        return sprites_dir
    
    # 初始化精灵目录
    SPRITES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprite")  # 使用绝对路径
    
    @staticmethod
    def my_bezier_func(t, d0, d1, d2, d3):
        """贝塞尔曲线计算"""
        return (1 - t) * ((1 - t) * ((1 - t) * d0 + t * d1) + t * ((1 - t) * d1 + t * d2)) + t * ((1 - t) * ((1 - t) * d1 + t * d2) + t * ((1 - t) * d2 + t * d3))
    
    def my_bezier(self, x, xa, ya, xb, yb):
        """计算贝塞尔曲线上的点"""
        xc = (xb + xa) / 2.0
        d = xb - xa
        t = float(x - xa) / float(d)
        y = WeatherDrawer.my_bezier_func(t, ya, ya, yb, yb)
        return int(y)
    
    def __init__(self):
        """初始化绘图器"""
        pass
    
    def time_diff_to_pixels(self, dt):
        """将时间差转换为像素"""
        ds = dt.total_seconds()
        seconds_per_pixel = (WeatherData.FORECAST_PERIOD_HOURS * 60 * 60) / WeatherDrawer.XSTEP
        return int(ds / seconds_per_pixel)
    
    def deg_to_pix(self, t):
        """将温度转换为像素位置"""
        n = (t - self.tmin) / self.degree_per_pixel
        y = self.ypos + self.YSTEP - int(n)
        return y
    
    def block_range(self, tline, x0, x1):
        """阻止指定范围的绘制"""
        for x in range(x0, x1):
            if x < len(tline):
                tline[x] = Sprites.DISABLED
    
    def draw_temperature(self, f, x, y, sprite):
        """绘制温度"""
        temp = f['temp'] if f['is_celsius'] else f['temp_fahrenheit']
        if f['is_celsius']:
            sprite.DrawInt(temp, x, y + 10, True, 2)
        else:
            sprite.DrawInt(temp, x, y + 10, False, 1)
    
    def draw_weather(self, weather_data):
        """绘制天气图"""
        # 创建空白图像 - 使用 'P' 模式创建索引图像
        img = Image.new('P', (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), color=1)  # 1=白色背景
        
        # 设置调色板（黑、白、红）
        palette = [0, 0, 0,       # 索引0=黑色
                  255, 255, 255,  # 索引1=白色
                  255, 0, 0]      # 索引2=红色
        
        # 填充剩余的调色板项（最多256种颜色）
        for i in range(3, 256):
            palette.extend([0, 0, 0])
            
        img.putpalette(palette)
        
        # 使用确保有效的精灵路径的方法
        sprites_dir = self.ensure_sprites_dir()
        
        # 初始化精灵
        sprite = Sprites(sprites_dir, img)
        
        self.pic_height = self.IMAGE_HEIGHT
        self.pic_width = self.IMAGE_WIDTH
        self.ypos = self.DRAWOFFSET
        
        # 计算可显示的预报数量
        n_forecast = ((self.pic_width - self.XSTART) / self.XSTEP)
        max_time = datetime.datetime.now() + datetime.timedelta(hours=WeatherData.FORECAST_PERIOD_HOURS * n_forecast)
        
        # 获取温度范围
        (self.tmin, self.tmax) = weather_data.get_temp_range(max_time)
        self.temp_range = self.tmax - self.tmin
        
        if self.temp_range < self.YSTEP:
            self.degree_per_pixel = self.DEFAULT_DEGREE_PER_PIXEL
        else:
            self.degree_per_pixel = self.temp_range / float(self.YSTEP)
        
        xpos = 0
        tline = [0] * (self.pic_width + self.XSTEP * 2)
        
        # 获取当前天气
        f = weather_data.get_current()
        old_temp = f['temp']
        old_y = self.deg_to_pix(old_temp)
        
        # 初始化温度线
        for i in range(self.XSTART):
            tline[i] = old_y
            
        # 绘制云层高度
        y_clouds = int(self.ypos - self.YSTEP / 2)
        
        # 绘制房屋
        sprite.Draw("house", 0, xpos, old_y)
        
        # 根据气压计算烟雾角度
        curr_hpa = f['pressure']
        smoke_angle_deg = ((curr_hpa - weather_data.pressure_min) / (weather_data.pressure_max - weather_data.pressure_min)) * 85 + 5
        
        if smoke_angle_deg < 0:
            smoke_angle_deg = 0
        if smoke_angle_deg > 90:
            smoke_angle_deg = 90
            
        # 绘制烟雾
        sprite.DrawSmoke(xpos + 21, self.pic_height - old_y + 23, smoke_angle_deg)
        
        # 绘制温度
        self.draw_temperature(f, xpos + 8, old_y, sprite)
        
        # 绘制云、雨和雪
        sprite.DrawCloud(f['clouds'], xpos, y_clouds, self.XSTART, self.YSTEP / 2)
        sprite.DrawRain(f['rain'], xpos, y_clouds, self.XSTART, tline)
        sprite.DrawSnow(f['snow'], xpos, y_clouds, self.XSTART, tline)
        
        # 当前时间
        t = datetime.datetime.now()
        
        # 每个预报点的时间间隔
        dt = datetime.timedelta(hours=WeatherData.FORECAST_PERIOD_HOURS)
        tf = t
        
        x0 = int(self.XSTART)
        xpos = x0
        n_forecast = int(n_forecast)
        
        # 绘制温度线
        n = int((self.XSTEP - self.XFLAT) / 2)
        for i in range(n_forecast + 1):
            f = weather_data.get_forecast_at_time(tf)
            if f is None:
                continue
                
            new_temp = f['temp']
            new_y = self.deg_to_pix(new_temp)
            
            # 使用贝塞尔曲线绘制温度线
            for i in range(n):
                if xpos + i < len(tline):
                    tline[xpos + i] = self.my_bezier(xpos + i, xpos, old_y, xpos + n, new_y)
            
            for i in range(self.XFLAT):
                if int(xpos + i + n) < len(tline):
                    tline[int(xpos + i + n)] = new_y
            
            xpos += n + self.XFLAT
            n = (self.XSTEP - self.XFLAT)
            old_temp = new_temp
            old_y = new_y
            tf += dt
        
        # 复制温度线
        tline0 = tline.copy()
        
        # 阻止起始区域的绘制
        self.block_range(tline, 0, x0)
        
        # 创建日出日落计算器
        sun_calc = SunCalculator(weather_data.lat, weather_data.lon)
        tf = t
        xpos = self.XSTART
        obj_counter = 0
        
        # 绘制日出日落
        for i in range(n_forecast + 1):
            f = weather_data.get_forecast_at_time(tf)
            if f is None:
                continue
            
            t_sunrise = sun_calc.sunrise(tf)
            t_sunset = sun_calc.sunset(tf)
            t_noon = datetime.datetime(tf.year, tf.month, tf.day, 12, 0, 0, 0)
            t_midn = datetime.datetime(tf.year, tf.month, tf.day, 0, 0, 0, 0) + datetime.timedelta(days=1)
            
            y_moon = self.ypos - self.YSTEP * 5 / 8
            
            # 绘制日出
            if (tf <= t_sunrise) and (tf + dt > t_sunrise):
                dx = self.time_diff_to_pixels(t_sunrise - tf) - self.XSTEP / 2
                sprite.Draw("sun", 0, xpos + dx, y_moon)
                obj_counter += 1
                if obj_counter == 2:
                    break
            
            # 绘制日落
            if (tf <= t_sunset) and (tf + dt > t_sunset):
                dx = self.time_diff_to_pixels(t_sunset - tf) - self.XSTEP / 2
                sprite.Draw("moon", 0, xpos + dx, y_moon)
                obj_counter += 1
                if obj_counter == 2:
                    break
            
            # 绘制中午标记
            if (tf <= t_noon) and (tf + dt > t_noon):
                dx = self.time_diff_to_pixels(t_noon - tf) - self.XSTEP / 2
                ix = int(xpos + dx)
                if ix < len(tline):
                    sprite.Draw("flower", 1, ix, tline[ix] + 1)
                    self.block_range(tline, ix - self.FLOWER_LEFT_PX, ix + self.FLOWER_RIGHT_PX)
            
            # 绘制午夜标记
            if (tf <= t_midn) and (tf + dt > t_midn):
                dx = self.time_diff_to_pixels(t_midn - tf) - self.XSTEP / 2
                ix = int(xpos + dx)
                if ix < len(tline):
                    sprite.Draw("flower", 0, ix, tline[ix] + 1)
                    self.block_range(tline, ix - self.FLOWER_LEFT_PX, ix + self.FLOWER_RIGHT_PX)
            
            xpos += self.XSTEP
            tf += dt
        
        # 绘制最高和最低温度
        is_tmin_printed = False
        is_tmax_printed = False
        tf = t
        xpos = self.XSTART
        n = int((self.XSTEP - self.XFLAT) / 2)
        f_used = []
        
        for i in range(n_forecast + 1):
            f = weather_data.get_forecast_at_time(tf)
            if f is None:
                continue
            
            dx = self.time_diff_to_pixels(f['time'] - tf) - self.XSTEP / 2
            ix = int(xpos + dx)
            
            y_clouds = int(self.ypos - self.YSTEP / 2)
            
            # 显示最低温度
            if (f['temp'] == self.tmin) and (not is_tmin_printed):
                if xpos + n < len(tline0):
                    self.draw_temperature(f, xpos + n, tline0[xpos + n], sprite)
                    is_tmin_printed = True
            
            # 显示最高温度
            if (f['temp'] == self.tmax) and (not is_tmax_printed):
                if xpos + n < len(tline0):
                    self.draw_temperature(f, xpos + n, tline0[xpos + n], sprite)
                    is_tmax_printed = True
            
            # 绘制风向、云、雨和雪
            if f not in f_used:
                sprite.DrawWind(f['windspeed'], f['winddeg'], ix, tline)
                sprite.DrawCloud(f['clouds'], ix, y_clouds, self.XSTEP, self.YSTEP / 2)
                sprite.DrawRain(f['rain'], ix, y_clouds, self.XSTEP, tline0)
                sprite.DrawSnow(f['snow'], ix, y_clouds, self.XSTEP, tline0)
                f_used.append(f)
            
            xpos += self.XSTEP
            tf += dt
        
        # 绘制温度线
        for x in range(self.pic_width):
            if x < len(tline0) and tline0[x] < self.pic_height:
                sprite.Dot(x, tline0[x], Sprites.BLACK)
        
        # 将索引模式图像转换为RGB模式，以便能够保存为JPEG格式
        img_rgb = img.convert('RGB')
        return img_rgb