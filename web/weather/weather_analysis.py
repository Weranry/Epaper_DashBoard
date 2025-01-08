from bs4 import BeautifulSoup

class WeatherAnalysis:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def get_weather_info(self):
        weather_info = {}

        # 提取当前时间
        current_time_tag = self.soup.find('p', class_='current-time')
        if current_time_tag:
            weather_info['current_time'] = current_time_tag.text.strip()

        # 提取温度和天气状况
        current_live_items = self.soup.find_all('div', class_='current-live__item')
        if current_live_items and len(current_live_items) > 1:
            weather_info['temperature'] = current_live_items[1].find('p').text.strip()
            weather_info['condition'] = current_live_items[1].find_all('p')[1].text.strip()

        # 提取空气质量
        aqi_tag = current_live_items[1].find('a', class_='air-tag')
        if aqi_tag:
            weather_info['aqi'] = aqi_tag.text.strip()

        # 提取天气摘要
        abstract_tag = self.soup.find('div', class_='current-abstract')
        if abstract_tag:
            weather_info['abstract'] = abstract_tag.text.strip()

        # 提取其他天气信息
        basic_items = self.soup.find_all('div', class_='current-basic___item')
        if basic_items:
            weather_info['wind'] = basic_items[0].find_all('p')[0].text.strip()
            weather_info['humidity'] = basic_items[1].find_all('p')[0].text.strip()
            weather_info['uv'] = basic_items[2].find_all('p')[0].text.strip()
            weather_info['feels_like'] = basic_items[3].find_all('p')[0].text.strip()
            weather_info['visibility'] = basic_items[4].find_all('p')[0].text.strip()
            weather_info['precipitation'] = basic_items[5].find_all('p')[0].text.strip()
            weather_info['pressure'] = basic_items[6].find_all('p')[0].text.strip()

        return weather_info 