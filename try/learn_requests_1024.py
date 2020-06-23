# -*-coding:utf8-*-
from lxml import etree
import requests
import os, shutil, threading, re, time, json
from concurrent.futures import ThreadPoolExecutor


# 每个详细页面名字的xpath地址     '//td[contains(@class,'tal')]/h3/a/font/text()'
# 每个详细页面的xpath地址    '//td[contains(@class,'tal')]/h3/a/@href'
# 图片xpath地址     '//img/@src'


def download(url):
    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        response.keep_alive = False
        response.encoding = 'gbk'
        if response.status_code != 200:
            print(f'这个地址的网页获取失败--{url}')
        return response
    except Exception as e:
        print(e, url)


def page_title_url(url):
    html1 = etree.HTML(res := download(url).text)
    # print(res)
    html_title = html1.xpath("//tr[@class='tr3 t_one tac']/td[contains(@class,'tal')]/h3/a//text()")
    pic_url_end = html1.xpath("//td[contains(@class,'tal')]/h3/a/@href")
    if len(html_title) != len(pic_url_end):
        raise ("详细页标题和地址数量不一致")
    html_url = map(lambda x: url_head + x, pic_url_end)
    return list(zip(html_title, html_url))


def down_one(url_one, dir_path, pic_name, index):
    file_name = '{}/{}-{}.jpg'.format(dir_path, pic_name, index)
    if (not os.path.exists(file_name)) and (pic_data := download(url_one).content):
        print('下载完一个图片 {}-{}'.format(pic_name, index))
        with open(file_name, 'wb') as f:
            f.write(pic_data)


def parse_2(page_adr, thread2):
    def doing():
        if (pic_down_adr := etree.HTML(download(v[1]).text).xpath("//img/@src")) and \
                v[0] not in PASS_TITLE:
            print(pic_down_adr)
            name = re.sub(rstr, "", v[0])
            dir_path = 'pic/{}'.format(name)
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                except OSError:
                    raise
                finally:
                    for index, url_one in enumerate(pic_down_adr):
                        time.sleep(1)
                        task = thread2.submit(down_one, url_one, dir_path, name, index)
                        ALL_TASK.append(task)
                        print("{}提交一个线程, {}-{}".format(threading.current_thread().name, name, index))
                        task.running()
                    print(len(ALL_TASK))
    for i, v in enumerate(page_adr):
        doing()


def url_head_new(headers):
    url_start = 'https://rr567.net/'
    headers['cookie'] = '__cfduid=d8820278eebccdea98714721a2976fa7b1569319655; _ga=GA1.2.829357220.1569319655; page=http%3A%2F%2Frvedc.com; _gid=GA1.2.334072831.1590379178; fuck1=yes'
    print("准备获取新地址")
    res = requests.get(url_start, headers=headers, timeout=30).text
    try:
        head = re.search(r"href='h.*?'", res).group()[6:-1]
        print("获取新地址成功")
        return head
    except TypeError:
        print('在首页获取1024网址出错')


def store_return_url(url=None):
    url_temp = None
    sign = 0
    with open('url_head.json', 'r') as f:
        try:
            head_list = json.load(f)
        except json.decoder.JSONDecodeError:
            head_list = []
        if yanzheng_url(url):
            print(f"新获取的地址可以使用{url}")
            url_temp = url
            if url not in head_list:
                head_list.append(url)
                sign = 1
        else:
            print('新地址不可使用，从存储的地址中获取')
            for i in head_list:
                print(f'测试地址{i}')
                if yanzheng_url(i):
                    url_temp = i
                    break
    if sign == 1:
        with open('url_head.json', 'w') as f:
            json.dump(head_list, f)
            print(f"加入新地址--{url}")
    if url_temp:
        return url_temp, head_list
    else:
        print('没有可用的地址')


def yanzheng_url(url):
    try:
        res = requests.get(url, timeout=3)
    except requests.exceptions.ReadTimeout:
        return False
    if res.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    ALL_TASK = []
    PASS_TITLE = ['[岛叔原创]怎么上传图片发布在论坛共享的简单图文教程', '草榴官方客戶端 & 大陸入口 & 永久域名  必須加入收藏夾 9.13更新', '各类图片上传的图床[更新7-28]', '自拍区发帖前必读(最新版）', '[技术贴]再现(寡人教程)之发图详解, 其實发图很簡單, 新手必學!', '为什么你的帖子没有得到评分？', '图区禁止使用下列图床，违者永久禁言，屏蔽IP', '發圖貼會員&訪客須知']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                 '(KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    headers = {'user-agent': user_agent}
    thread2 = ThreadPoolExecutor(max_workers=1)
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    if not os.path.isdir('pic/'):
        os.mkdir('pic/')
    total_pages = 2
    url_index, _ = store_return_url(url_head_new(headers))
    url_head = url_index[:-9]
    url_list = ['{}thread0806.php?fid=16&search=&page={}'.format(url_head, i) for i in range(1, total_pages)]
    print(url_list)
    for url in url_list:
        page_adr = page_title_url(url)
        print(page_adr)
        parse_2(page_adr,  thread2)
    # for j in ALL_TASK:
        # print(j.done())
    thread2.shutdown(wait=True)









