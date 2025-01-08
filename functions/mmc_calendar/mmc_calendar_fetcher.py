import requests
import time

def fetch_mmc_calendar_image(channel):
    url = "http://mmc-prod-max.mmc-data.com/Calendar/api/image/get/device/image/"
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "MMC_WiFi/S.0.5.0",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }

    current_timestamp = int(time.time())

    data = {
        "device_id_ex": "cc50e3fc2b98",
        "channel_list": [
            {
                "channel": channel,
                "images_date": [str(current_timestamp)]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return None  # 返回None表示请求失败

    response_json = response.json()  # 解析JSON响应
    if 'images' not in response_json or not response_json['images']:
        return None  # 返回None表示没有图像

    image_url = response_json['images'][0]['iamge_url']  # 获取图像URL
    return image_url 