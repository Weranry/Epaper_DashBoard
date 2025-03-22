import sys
import requests
from bs4 import BeautifulSoup
import re

def get_wiki_page():
    """
    获取中文维基百科首页内容（简体中文版本）
    
    返回:
        BeautifulSoup对象
    """
    # 使用简体中文版本的URL
    url = "https://zh.wikipedia.org/zh-cn/Wikipedia:%E9%A6%96%E9%A1%B5"
    
    # 设置用户代理来模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 发送GET请求到URL
    response = requests.get(url, headers=headers)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析HTML内容
        return BeautifulSoup(response.text, 'html.parser')
    else:
        raise Exception(f"获取网页失败。状态码: {response.status_code}")

def get_featured_article(soup):
    """
    获取典范条目内容
    
    参数:
        soup: BeautifulSoup对象
    
    返回:
        包含典范条目内容的字典
    """
    result = {"典范条目": []}
    
    # 查找典范条目标题
    headings = soup.find_all('h2')
    for heading in headings:
        heading_text = heading.get_text().strip()
        if "典范条目" in heading_text:
            # 找到了目标标题，获取其父元素的div
            parent_div = heading.find_parent('div', class_='mp-2012-column-left-block') or \
                         heading.find_parent('div', class_='mp-2012-column-right-subblock')
            
            if parent_div:
                # 找到内容区域
                content_div = parent_div.find('div', class_='knoblock') or \
                              parent_div.find('div', class_='mp-2012-text')
                
                if content_div:
                    # 典范条目通常是一段连续文本
                    text = content_div.get_text().strip()
                    text = re.sub(r'\s+', ' ', text)
                    result["典范条目"].append(text)
    
    return result

def get_news(soup):
    """
    获取新闻动态内容（所有条目），排除"正在发生"和"最近逝世"相关内容
    
    参数:
        soup: BeautifulSoup对象
    
    返回:
        包含新闻动态内容的字典
    """
    result = {"新闻动态": []}
    
    # 查找新闻动态标题
    headings = soup.find_all('h2')
    for heading in headings:
        heading_text = heading.get_text().strip()
        if "新闻动态" in heading_text:
            # 找到了目标标题，获取其父元素的div
            parent_div = heading.find_parent('div', class_='mp-2012-column-left-block') or \
                         heading.find_parent('div', class_='mp-2012-column-right-subblock')
            
            if parent_div:
                # 找到内容区域
                content_div = parent_div.find('div', class_='knoblock') or \
                              parent_div.find('div', class_='mp-2012-text')
                
                if content_div:
                    # 新闻动态通常是列表项
                    list_items = content_div.find_all('li')
                    # 获取所有条目
                    for item in list_items:
                        text = item.get_text().strip()
                        # 去掉"（图）"标记
                        text = re.sub(r'（图）', '', text)
                        text = re.sub(r'\s+', ' ', text)
                        
                        # 排除包含"正在发生"和"最近逝世"的条目，避免重复
                        if not ("正在发生" in text or "最近逝世" in text):
                            result["新闻动态"].append(text)
    
    return result

def get_did_you_know(soup):
    """
    获取你知道吗？内容（所有条目）
    
    参数:
        soup: BeautifulSoup对象
    
    返回:
        包含你知道吗？内容的字典
    """
    result = {"你知道吗？": []}
    
    # 查找你知道吗？标题
    headings = soup.find_all('h2')
    for heading in headings:
        heading_text = heading.get_text().strip()
        if "你知道吗？" in heading_text:
            # 找到了目标标题，获取其父元素的div
            parent_div = heading.find_parent('div', class_='mp-2012-column-left-block') or \
                         heading.find_parent('div', class_='mp-2012-column-right-subblock')
            
            if parent_div:
                # 找到内容区域
                content_div = parent_div.find('div', class_='knoblock') or \
                              parent_div.find('div', class_='mp-2012-text')
                
                if content_div:
                    # 你知道吗？通常是列表项
                    list_items = content_div.find_all('li')
                    # 获取所有条目
                    for item in list_items:
                        text = item.get_text().strip()
                        # 去掉"（图）"标记
                        text = re.sub(r'（图）', '', text)
                        text = re.sub(r'\s+', ' ', text)
                        result["你知道吗？"].append(text)
    
    return result

def get_ongoing_and_deaths(soup):
    """
    获取正在发生和最近逝世内容
    
    参数:
        soup: BeautifulSoup对象
    
    返回:
        包含正在发生和最近逝世内容的字典
    """
    result = {"热点事件": []}
    
    # 查找"正在发生"和"最近逝世"部分
    ongoing_events = []
    recent_deaths = []
    
    # 查找包含这些部分的div
    feature_more_divs = soup.find_all('div', id='column-feature-more')
    for div in feature_more_divs:
        spans = div.find_all('span', class_='column-feature-more-header')
        for span in spans:
            header_text = span.get_text().strip()
            if "正在发生" in header_text:
                ongoing_events_span = span.find_next('span', class_='hlist inline')
                if ongoing_events_span:
                    links = ongoing_events_span.find_all('a')
                    # 获取所有正在发生的事件
                    for link in links:
                        ongoing_events.append(link.get_text().strip())
            elif "最近逝世" in header_text:
                recent_deaths_span = span.find_next('span', class_='hlist inline')
                if recent_deaths_span:
                    links = recent_deaths_span.find_all('a')
                    # 获取所有最近逝世的人物
                    for link in links:
                        recent_deaths.append(link.get_text().strip())
    
    # 将正在发生的事件作为单独的一行
    if ongoing_events:
        result["热点事件"].append(f"正在发生: {' '.join(ongoing_events)}")
    
    # 将最近逝世的人物作为单独的一行
    if recent_deaths:
        result["热点事件"].append(f"最近逝世: {' '.join(recent_deaths)}")
    
    return result

def get_all_wiki_content():
    """
    获取所有维基百科内容
    
    返回:
        包含所有部分内容的字典
    """
    soup = get_wiki_page()
    
    # 获取各部分内容
    featured_article = get_featured_article(soup)
    news = get_news(soup)
    did_you_know = get_did_you_know(soup)
    ongoing_and_deaths = get_ongoing_and_deaths(soup)
    
    # 合并所有内容
    all_content = {}
    all_content.update(featured_article)
    all_content.update(news)
    all_content.update(did_you_know)
    all_content.update(ongoing_and_deaths)
    
    return all_content