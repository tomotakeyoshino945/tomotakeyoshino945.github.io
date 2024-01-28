import os
import re
import requests
import time

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 ",
    }
    html = requests.get(url, headers=headers).text
    return html

def parse_html(html_text):
    picre = re.compile(r'[a-zA-z]+://[^\s]*\.jpg')  # 本正则式得到.jpg结尾的url
    pic_list = []
    for pic_url in picre.findall(html_text):
        match = re.search(r'\d{5,}', pic_url)
        if match:
            pic_list.append(match.group())
    return pic_list


def main():
    for page in range(1, 131):
        url = 'https://hanime1.me/tags/%E7%84%A1%E7%A2%BC?page=' + str(page)
        html_text = get_html(url)
        pic_list = parse_html(html_text)
        with open('ID.txt', 'a') as f:  # 使用追加模式打开文件，将结果追加到文件末尾
            for pic_url in pic_list:
                f.write(pic_url + '\n')
        time.sleep(1)  # 添加延时，避免请求过于频繁被网站屏蔽


if __name__ == '__main__':
    main()
