import os
import re
import requests
import time

def download(file_path, picture_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    }
    max_retries = 8  # 最大重试次数
    for i in range(max_retries):
        try:
            r = requests.get(picture_url, headers=headers)
            with open(file_path, 'wb') as f:
                f.write(r.content)
            break  # 如果下载成功，退出循环
        except requests.exceptions.RequestException as e:
            print(f'Retry {i+1}/{max_retries} after {e}')
            time.sleep(2**(i+1))  # 指数增长的延迟重试

def main():
    with open('./List/Target_1.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        m = int(line.strip())  # 从每行读取的数字  
        prefix_url = 'https://i.nhentai.net/galleries/'+ str(m) +'/'  # 同一类目下的图片url前缀
        prefix_url_t = 'https://t.nhentai.net/galleries/'+ str(m) +'/' 
        match = re.search(r'\d+', prefix_url)
        if match:
            webname = match.group()
        else:
            print('No match found')
        os.makedirs('./Book/' + webname + '/', exist_ok=True)  # 输出目录

        # 下载cover.jpg
        cover_file_path = './Book/' + webname + '/cover.jpg'
        cover_picture_url = prefix_url_t + 'cover.jpg'
        download(cover_file_path, cover_picture_url)

        n = 1000  # 该类目下的图片下载最大数
        tmp = prefix_url.split('/')[-1]
        prev_sizes = [None,None]  # 存储前两张图片的大小
        for i in range(1, n + 1):
            file_path = './Book/' + webname + '/' + tmp + str(i) + '.jpg'
            picture_url = prefix_url + str(i) + '.jpg'
            download(file_path, picture_url)

            # 检查前两张图片的大小
            if i > 2:
                current_size = os.path.getsize(file_path)
                if prev_sizes[0] == prev_sizes[1] == current_size:
                    print(f'连续三张图片大小相同，停止下载！')
                    break

            # 更新前两张图片的大小列表
            if i > 1:
                prev_sizes.pop(0)
            prev_sizes.append(os.path.getsize(file_path))

if __name__ == '__main__':
    main()
