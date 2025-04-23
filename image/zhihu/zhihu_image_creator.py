import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from bs4 import BeautifulSoup
import os
from lib.qrcode.qrcode_generator import generate_qr_code  # 导入二维码生成器
from lib.date.date_calculator import DateCalculator  # 导入日期计算器

class ZhihuImageCreator:
    def __init__(self):
        font_path = os.path.join('assets', 'simhei.ttc')
        self.font = ImageFont.truetype(font_path, 32)
        self.date_calculator = DateCalculator()  # 实例化日期计算器

    def fetch_and_extract_zhihu(self):
        url = 'https://rss.weranry.com/zhihu/daily'
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            xml_data = response.text

            # 使用 BeautifulSoup 解析 XML
            soup = BeautifulSoup(xml_data, 'html.parser')
            first_item = soup.find('item')

            title = first_item.find('title').text
            link = first_item.find('link').text

            return {
                "title": title,
                "link": link
            }
        except Exception as e:
            print('获取或解析HTML时出错:', e)
            return None

    def create_zhihu_image(self):
        zhihu_data = self.fetch_and_extract_zhihu()
        if not zhihu_data:
            return None

        width, height = 400, 300
        img = Image.new('P', (width, height))
        img.putpalette([
            255, 255, 255,  # 白色
            0, 0, 0,        # 黑色
            255, 0, 0       # 红色
        ])
        draw = ImageDraw.Draw(img)

        # 获取日期信息
        solar_date = self.date_calculator.get_solar_date()
        month = solar_date['solar_month']
        day = solar_date['solar_day']
        week_day = solar_date['weekday']

        # 绘制日期和星期
        draw.text((10, 10), f"{month}月{day}日 | {week_day}", font=self.font, fill=1)

        # 绘制知乎标题
        draw.text((10, 50), zhihu_data['title'], font=self.font, fill=1)

        # 生成二维码
        qr_code_img = generate_qr_code(zhihu_data['link'])
        qr_code_img = qr_code_img.resize((100, 100))  # 调整二维码大小
        img.paste(qr_code_img, (width - 110, 10))  # 将二维码粘贴到图片上

        # 转换为24位RGB图像
        img = img.convert('RGB')

        # 创建图像
        im = Image.frombytes('1', (height, width), img.tobytes())
        im2 = im.transpose(method=Image.TRANSPOSE)

        # 添加空白区域
        new_height = 800
        new_image = Image.new('RGB', (width, new_height), (255, 255, 255))  # 创建白色背景的新图像
        new_image.paste(im2, (0, (new_height - height) // 2))  # 将原图像粘贴到新图像的中心

        # 保存图像为JPEG格式
        output_path = os.path.join(os.path.dirname(__file__), 'output_image.jpeg')
        new_image.save(output_path, 'JPEG')

        return new_image

    def get_image_bytes(self, img):
        img_io = BytesIO()
        # 保存为JPEG，使用最高质量
        img.save(img_io, 'JPEG', quality=95, subsampling=0)  # 4:4:4 subsampling
        img_io.seek(0)
        return img_io 