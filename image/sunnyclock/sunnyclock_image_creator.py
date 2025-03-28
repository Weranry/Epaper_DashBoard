from PIL import Image, ImageDraw, ImageFont
import datetime
import pytz
from io import BytesIO
import os
from web.sunnyclock.fetch_sunnyclock import get_sunnyclock_data

class SunnyClockImageCreator:
    def __init__(self):
        font_path = os.path.join('assets', 'simhei.ttc')
        self.text_font = ImageFont.truetype(font_path, 16)
        self.title_font = ImageFont.truetype(font_path, 24)
        self.time_font = ImageFont.truetype(font_path, 14)
        
        # 尝试加载额外的图标字体
        icon_font_path = os.path.join('assets', 'sunnyclock.ttf')
        try:
            self.icon_font = ImageFont.truetype(icon_font_path, 18)
        except:
            # 如果找不到图标字体，使用普通字体替代
            print(f"警告: 找不到图标字体 '{icon_font_path}'，使用普通字体替代")
            self.icon_font = self.text_font
        
    # 将以下方法修改为实例方法，添加self参数
    def map_cloudcover(self, value):
        # 云量1-9映射到
        mapping = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: ''}
        return mapping.get(value, '')

    def map_seeing(self, value):
        # 视宁度1-8映射到
        mapping = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''}
        return mapping.get(value, '')

    def map_transparency(self, value):
        # 透明度1-8映射到
        mapping = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''}
        return mapping.get(value, '')

    def map_lifted_index(self, value):
        # 稳定度0-15映射为数字，其他范围映射为字母
        if 0 <= value <= 15:
            return str(value)
        elif -3 < value <= 0:
            return  ''
        elif -5 <= value <= -3:
            return  ''
        elif value < -5:
            return  ''
        return ''

    def map_rh2m(self, value):
        # 湿度1,2,3映射到
        mapping = {1: '', 2: '', 3: ''}
        return mapping.get(value, '')

    def map_prec_type(self, value):
        # 降水类型映射
        mapping = {'snow': '', 'rain': '', 'none': ''}
        return mapping.get(value, '')

    def map_wind_direction(self, value):
        # 八个风向映射到箭头方向
        mapping = {
            "N": "↑",    # 北
            "NE": "↗",   # 东北
            "E": "→",    # 东
            "SE": "↘",   # 东南
            "S": "↓",    # 南
            "SW": "↙",   # 西南
            "W": "←",    # 西
            "NW": "↖"    # 西北
        }
        return mapping.get(value, "")
        
    def create_sunnyclock_image(self, lat, lon):
        # 创建新图片 - 使用索引颜色模式
        img_width = 400
        img_height = 300
        img = Image.new('P', (img_width, img_height))
        
        # 设置调色板为白、黑、红
        img.putpalette([
            255, 255, 255,  # 白色 (索引 0)
            0, 0, 0,        # 黑色 (索引 1)
            255, 0, 0       # 红色 (索引 2)
        ])
        
        draw = ImageDraw.Draw(img)
        
        # 获取天气数据
        sunnyclock_data = get_sunnyclock_data(lon, lat)
        
        # 获取当前UTC时间，然后转换为北京时间
        utc_now = datetime.datetime.now(pytz.UTC)
        beijing_time = utc_now.astimezone(pytz.timezone('Asia/Shanghai'))
        update_time = beijing_time.strftime("%Y-%m-%d %H:%M")
        
        # 布局参数
        title_height = 37  # 标题区域高度
        bottom_height = 15  # 底部信息高度
        
        # 计算表格可用高度
        table_height = img_height - title_height - bottom_height
        
        # 表格有10行（标题行+9个数据行）
        row_height = table_height // 10
        
        # 列宽度计算
        param_width = 70  # 第一列宽度
        data_width = (img_width - param_width) // 8  # 8个数据列
        
        # 绘制标题
        title = "晴天钟"
        title_width = draw.textlength(title, font=self.title_font)
        draw.text(((img_width - title_width) // 2, 3), title, fill=1, font=self.title_font)
        
        # 表格起始坐标
        x_start = 0
        y_start = title_height
        
        # 绘制表头行
        # 参数列
        draw.rectangle([x_start, y_start, x_start+param_width, y_start+row_height], outline=1)
        text = "时间"
        text_width = draw.textlength(text, font=self.text_font)
        draw.text((x_start+(param_width-text_width)//2, y_start+(row_height-self.text_font.size)//2), text, fill=1, font=self.text_font)
        
        # 时间点列
        for i, timepoint in enumerate(sunnyclock_data["timepoints"][:8]):
            x = x_start + param_width + i * data_width
            draw.rectangle([x, y_start, x+data_width, y_start+row_height], outline=1)
            text = f"{timepoint}h"
            text_width = draw.textlength(text, font=self.text_font)
            draw.text((x+(data_width-text_width)//2, y_start+(row_height-self.text_font.size)//2), text, fill=1, font=self.text_font)
        
        # 数据行
        param_names = ["云量", "视宁度", "透明度", "不稳定度", "湿度", "风向", "风速", "温度", "降水类型"]
        data_keys = ["cloudcover", "seeing", "transparency", "lifted_index", "rh2m", 
                    "wind_direction", "wind_speed", "temp2m", "prec_type"]
        is_icon = [True, True, True, False, True, False, False, False, True]  # 标记哪些使用icon字体
        
        current_y = y_start + row_height
        
        for row_idx, (param_name, key, use_icon) in enumerate(zip(param_names, data_keys, is_icon)):
            # 参数名
            draw.rectangle([x_start, current_y, x_start+param_width, current_y+row_height], outline=1)
            text_width = draw.textlength(param_name, font=self.text_font)
            draw.text((x_start+(param_width-text_width)//2, current_y+(row_height-self.text_font.size)//2), 
                    param_name, fill=1, font=self.text_font)
            
            # 数据值
            for i, value in enumerate(sunnyclock_data[key][:8]):
                x = x_start + param_width + i * data_width
                draw.rectangle([x, current_y, x+data_width, current_y+row_height], outline=1)
                
                # 根据不同参数处理显示内容
                if key == "cloudcover":
                    content = self.map_cloudcover(value)
                elif key == "seeing":
                    content = self.map_seeing(value)
                elif key == "transparency":
                    content = self.map_transparency(value)
                elif key == "lifted_index":
                    content = self.map_lifted_index(value)
                elif key == "rh2m":
                    content = self.map_rh2m(value)
                elif key == "wind_direction":
                    content = self.map_wind_direction(value)
                elif key == "prec_type":
                    content = self.map_prec_type(value)
                else:
                    content = str(value)
                
                # 选择合适的字体并居中绘制
                if use_icon:
                    font = self.icon_font
                else:
                    font = self.text_font
                
                # 完全居中（水平和垂直）
                text_width = draw.textlength(content, font=font)
                draw.text((x+(data_width-text_width)//2, current_y+(row_height-font.size)//2), 
                        content, fill=1, font=font)
            
            current_y += row_height
        
        # 表格下方显示更新时间
        info_text = f"更新时间: {update_time}"
        text_width = draw.textlength(info_text, font=self.time_font)
        draw.text((3, img_height - bottom_height + (bottom_height-self.time_font.size)//2 - 5), 
                info_text, fill=1, font=self.time_font)
        
        # 转换为RGB模式以确保保存为高质量JPEG
        rgb_img = img.convert('RGB')
        
        return rgb_img
    
    def get_image_bytes(self, img):
        """将图像转换为字节流"""
        img_io = BytesIO()
        # 保存为JPEG，使用最高质量
        img.save(img_io, 'JPEG', quality=95, subsampling=0)  # 4:4:4 subsampling
        img_io.seek(0)
        return img_io