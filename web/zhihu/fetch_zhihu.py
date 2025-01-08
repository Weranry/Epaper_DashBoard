import requests
from bs4 import BeautifulSoup

def fetch_and_extract_zhihu():
    url = 'https://rss.weranry.com/zhihu/daily'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        xml_data = response.text

        # 使用 BeautifulSoup 解析 XML，使用 html.parser 作为解析器
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