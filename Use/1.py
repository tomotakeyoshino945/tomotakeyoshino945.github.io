import os
import re
import requests
import time

def download(file_path, picture_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    }
    max_retries = 3  # 最大重试次数
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
	prefix_url = 'https://i.nhentai.net/galleries/2800676/'  # 同一类目下的图片url前缀
	match = re.search(r'\d+', prefix_url)
	if match:
		webname = match.group()
	else:
		print('No match found')
	output_dir = f'./pic/{webname}/'
	os.makedirs(output_dir, exist_ok=True)  # 输出目录


	n =  300 # 该类目下的图片总数

	tmp = prefix_url.split('/')[-1]
	for i in range(1, n + 1):
		file_path = output_dir + tmp + str(i) + '.jpg'
		picture_url = prefix_url + str(i) + '.jpg'
		download(file_path, picture_url)
		time.sleep(1)
		

if __name__ == '__main__':
	main()