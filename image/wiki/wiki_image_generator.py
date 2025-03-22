import sys
from PIL import Image, ImageDraw, ImageFont, ImagePalette
import textwrap
import os
from io import BytesIO
from datetime import datetime
from web.wiki.wiki_scraper import get_all_wiki_content



class WikiImageCreator:
    def __init__(self, font_path="simhei.ttc"):
        # 检查字体文件是否存在于当前目录或assets目录
        if not os.path.exists(font_path):
            font_dir = os.path.join("assets", "fonts")
            self.font_path = os.path.join(font_dir, os.path.basename(font_path))
            # 如果fonts目录不存在，则检查assets目录
            if not os.path.exists(self.font_path):
                self.font_path = os.path.join("assets", os.path.basename(font_path))
        else:
            self.font_path = font_path
    
    def create_wiki_image(self, width=480, height=800):
        """
        创建包含维基百科内容的图像，适用于电子墨水屏
        
        参数:
            width: 图像宽度 (暂时固定为480)
            height: 图像高度 (暂时固定为800)
            
        返回:
            PIL图像对象
        """
        # 注意：目前参数width和height被忽略，使用固定值
        # 这部分代码被保留，以便将来可能需要调整尺寸时使用
        width = 480  # 固定宽度
        height = 800  # 固定高度
        
        # 获取维基百科内容
        wiki_content = get_all_wiki_content()
        
        # 创建一个索引颜色图像（为避免抗锯齿）
        # 使用调色板图像以确保文本渲染没有抗锯齿
        image = Image.new('P', (width, height), color=0)  # 0 表示白色
        
        # 创建黑白调色板
        palette = [255, 255, 255]  # 索引0是白色
        palette.extend([0, 0, 0])  # 索引1是黑色
        palette.extend([255, 0, 0])  # 索引2是红色
        
        # 填充剩余调色板
        for i in range(3, 256):
            palette.extend([255, 255, 255])
        
        # 设置调色板
        image.putpalette(palette)
        
        # 将图像填充为白色
        ImageDraw.Draw(image).rectangle([(0, 0), (width, height)], fill=0)
        
        draw = ImageDraw.Draw(image)
        
        # 加载字体
        title_font = ImageFont.truetype(self.font_path, size=18)
        section_font = ImageFont.truetype(self.font_path, size=16)
        content_font = ImageFont.truetype(self.font_path, size=14)
        
        # 设置边距和行高
        margin_x = 5
        margin_y = 10
        content_x = 12  # 内容缩进
        max_width = 475  # 设置为475，按要求
        
        # 调整行高
        line_height_title = 24
        line_height_section = 20
        line_height_content = 18
        item_spacing = 2  # 项目间的额外间距
        section_spacing = 8  # 章节之间的额外间距
        
        # 定义要显示的部分及其顺序（按照用户要求调整）
        sections_order = ["热点事件", "新闻动态", "你知道吗？", "典范条目"]
        
        # 获取当前日期
        current_date = datetime.now().strftime("%m月%d日")
        
        # 绘制页面标题和日期在同一行（居中）
        y = margin_y
        title_text = f"{current_date}维基百科摘要"
        # 计算标题宽度以实现居中
        title_width = draw.textlength(title_text, font=title_font)
        draw.text(((width - title_width) // 2, y), title_text, font=title_font, fill=1)  # 黑色(索引1)
        y += line_height_title
        
        # 绘制分隔线
        draw.line([(margin_x, y), (width - margin_x, y)], fill=1, width=1)  # 黑色(索引1)
        y += 8
        
        # 创建一个文本换行函数，改进换行逻辑
        def wrap_text(text, font, max_width):
            """改进的文本换行函数，更好地处理长单词和中英文混合文本"""
            if not text:
                return []
                
            # 如果文本宽度小于最大宽度，则直接返回
            if draw.textlength(text, font=font) <= max_width:
                return [text]
                
            # 对于中英文混合的文本，按照宽度拆分
            lines = []
            current_line = ""
            for char in text:
                # 测试添加下一个字符后的宽度
                test_line = current_line + char
                width = draw.textlength(test_line, font=font)
                
                if width <= max_width:
                    current_line = test_line
                else:
                    # 当前行已达到最大宽度，保存并重新开始
                    lines.append(current_line)
                    current_line = char
                    
            # 添加最后一行
            if current_line:
                lines.append(current_line)
                
            return lines
        
        # 定义各部分的最大行数
        max_lines = {
            "热点事件": 2,  # 正在发生和最近逝世各占一行
            "新闻动态": 10,
            "你知道吗？": 10,
            "典范条目": 12
        }
        
        # 显示各个部分内容
        for section_name in sections_order:
            if section_name in wiki_content and wiki_content[section_name]:
                # 绘制部分标题
                draw.text((margin_x, y), f"【{section_name}】", font=section_font, fill=1)  # 黑色(索引1)
                y += line_height_section
                
                # 绘制部分内容
                content_list = wiki_content[section_name]
                
                # 处理各个部分的内容
                lines_used = 0
                for item in content_list:
                    # 如果已经达到该部分的最大行数，停止处理
                    if lines_used >= max_lines[section_name]:
                        break
                    
                    # 处理不同类型的内容格式
                    if section_name == "典范条目" or item.startswith("正在发生:") or item.startswith("最近逝世:"):
                        display_text = item
                    else:
                        # 使用 · 替代数字序号
                        display_text = f"· {item}"
                    
                    # 使用改进的换行函数
                    wrapped_lines = wrap_text(display_text, content_font, max_width - (content_x - margin_x))
                    
                    # 限制每个项目使用的行数
                    remaining_lines = max_lines[section_name] - lines_used
                    if len(wrapped_lines) > remaining_lines:
                        wrapped_lines = wrapped_lines[:remaining_lines]
                        # 如果文本被截断，在最后一行添加省略号
                        if wrapped_lines:
                            last_line = wrapped_lines[-1]
                            # 检查添加省略号后是否超出宽度
                            if draw.textlength(last_line + "...", font=content_font) <= max_width - (content_x - margin_x):
                                wrapped_lines[-1] = last_line + "..."
                            else:
                                # 如果会超出宽度，截断最后一行以容纳省略号
                                while draw.textlength(last_line + "...", font=content_font) > max_width - (content_x - margin_x):
                                    last_line = last_line[:-1]
                                wrapped_lines[-1] = last_line + "..."
                    
                    # 绘制文本行
                    for line in wrapped_lines:
                        draw.text((content_x, y), line, font=content_font, fill=1)  # 黑色(索引1)
                        y += line_height_content
                        lines_used += 1
                    
                    # 如果已经达到该部分的最大行数，停止处理
                    if lines_used >= max_lines[section_name]:
                        break
                    
                    # 项目之间添加间距（如果还有空间）
                    if lines_used < max_lines[section_name]:
                        y += item_spacing
                
                # 如果使用的行数少于最大行数，将y坐标调整到应有的位置
                if lines_used < max_lines[section_name]:
                    # 计算应该增加的高度以达到预留的空间
                    remaining_lines = max_lines[section_name] - lines_used
                    y += remaining_lines * line_height_content
                
                # 部分之间添加额外间距和分隔线
                y += section_spacing
                if section_name != "典范条目" and y < height - line_height_content:
                    draw.line([(margin_x, y - section_spacing//2), (width - margin_x, y - section_spacing//2)], 
                            fill=1, width=1)  # 黑色(索引1)
        
        # 将索引颜色图像转换为RGB图像
        rgb_image = image.convert('RGB')
        
        return rgb_image
    
    def get_image_bytes(self, img):
        """将PIL图像对象转换为字节流"""
        img_io = BytesIO()
        # 保存为JPEG，使用最高质量
        img.save(img_io, 'JPEG', quality=95, subsampling=0)  # 4:4:4 subsampling
        img_io.seek(0)
        return img_io