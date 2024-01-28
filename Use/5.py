import os
import re
import requests
import time

def get_html(url, max_retries=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 ",
    }
    for i in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 如果响应码不为200，会抛出异常
            html = response.text
            return html  # 如果成功获取到HTML，直接返回
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f'Retry {i+1}/{max_retries} after {e}')
            time.sleep(2**(i+1))  # 指数增长的延迟重试
    raise Exception(f'Failed to get HTML after {max_retries} retries')  # 如果多次重试仍然失败，抛出异常

from bs4 import BeautifulSoup

def parse_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    div_list = soup.find_all('div', class_='comic-rows-videos-title')
    title_list = []
    for div in div_list:
        title = div.text.strip()
        title_list.append(title)
    return title_list

def main():
    for page in range(1, 131):
        url = 'https://hanime1.me/tags/%E7%84%A1%E7%A2%BC?page=' + str(page)
        html_text = get_html(url)
        title_list = parse_html(html_text)
        with open('Title.txt', 'a', encoding='UTF-8') as f:  # 使用追加模式打开文件，将结果追加到文件末尾
                    for title in title_list:
                        f.write(title + '\n')
                        time.sleep(0.5)  # 添加延时，避免请求过于频繁被网站屏蔽

if __name__ == '__main__':
    main()
