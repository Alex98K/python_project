import re, requests


url_one = 'https://www.sinaimg.cn/dy/slidenews/32_img/2016_33/35533_5251718_971332.gi\\f<>|?'
style = re.sub(r'[\/\\\:\*\?\"\<\>\|]', '', url_one)
print(style)
title = '包从精液母狗堕落到肉便器公厕的日常第一番（温泉外露加穿阴环'
PASS_TITLE = ['hah', '肉便']
print(list(filter(lambda x: x in title, PASS_TITLE)))
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                 '(KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
headers = {'user-agent': user_agent}

def download(html_url):  # 下载器，将传入的url地址进行get请求，获取返回页面
    try:
        response = requests.get(url=html_url, headers=headers, timeout=100, allow_redirects=True)
        response.keep_alive = False
        response.encoding = 'gbk'
        if response.status_code != 200:
            print(f'这个地址的网页获取失败--{html_url}')
        return response
    except Exception as e:
        print(e, html_url)

print(download('https://cl.ff0.xyz/htm_data/2007/16/3974973.html').text)