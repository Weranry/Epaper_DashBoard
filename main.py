from flask import Flask, make_response
from PIL import Image, ImageDraw, ImageFont
import io


app = Flask(__name__)


@app.route('/get_image', methods=['GET'])
def get_image():
    # 创建一个400x300的黑色背景图片（这里尺寸符合4.2寸屏幕要求）
    img = Image.new('P', (400, 300), color = 0)
    palette = img.getpalette()
    palette[:9] = [255, 255, 255, 0, 0, 0, 255, 0, 0]
    img.putpalette(palette)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('simhei.ttf', size = 30)
    draw.text((10, 10), "Hello World", font = font, fill = 255)
    draw.text((10, 50), "你好世界", font = font, fill = 255)
    img = img.convert('RGB')

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality = 95, subsampling = 0)
    img_byte_arr = img_byte_arr.getvalue()

    response = make_response(img_byte_arr)
    response.headers.set('Content-Type', 'image/jpeg')
    return response


if __name__ == '__main__':
    app.run(debug = True)
