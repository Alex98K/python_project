# -*-coding:utf8-*-
from lxml import etree
import requests
import os, shutil, threading, re, time, json
from concurrent.futures import ThreadPoolExecutor


# 每个详细页面名字的xpath地址     '//td[contains(@class,'tal')]/h3/a/font/text()'
# 每个详细页面的xpath地址    '//td[contains(@class,'tal')]/h3/a/@href'
# 图片xpath地址     '//img/@data-src'
ALL_TASK = []


def download(url):
    try:
        response = requests.get(url=url, headers=headers, timeout=60)
        response.keep_alive = False
        response.encoding = 'gbk'
        if response.status_code != 200:
            print(url)
        return response
    except Exception as e:
        print(e, url)


def parse_1(url):
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
        if (pic_down_adr := etree.HTML(download(v[1]).text).xpath("//img/@data-src")) and \
                v[0] != '[岛叔原创]怎么上传图片发布在论坛共享的简单图文教程':
            # print(pic_down_adr)
            name = re.sub(rstr, "", v[0])
            dir_path = 'pic/{}'.format(name)
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                except OSError:
                    raise
                finally:
                    for index, url_one in enumerate(pic_down_adr):
                        task = thread2.submit(down_one, url_one, dir_path, name, index)
                        ALL_TASK.append(task)
                        # print("{}提交一个线程, {}-{}".format(threading.current_thread().name, name, index))
                        task.running()
                    print(len(ALL_TASK))
    for i, v in enumerate(page_adr):
        doing()


def url_head_list(headers):
    url_start = 'https://rr567.net/'
    headers['cookie'] = '__cfduid=d8820278eebccdea98714721a2976fa7b1569319655; _ga=GA1.2.829357220.1569319655; page=http%3A%2F%2Frvedc.com; _gid=GA1.2.334072831.1590379178; fuck1=yes'
    res = requests.get(url_start, headers=headers).text
    print(res)
    try:
        head = re.search(r"href='h.*?'", res).group()[6:-1]
        return head
    except TypeError:
        print('在首页获取1024网址出错')


def store_url(url=None):
    url_temp = None
    with open('url_head.json', 'a') as f:
        res_head = json.loads(f)
        if yanzheng_url(url):
            url_temp = url
        if url not in res_head:
            if res_head == None:
                res_head = []
            res_head.append(url)
            json.dumps(res_head)
            print(f"加入新地址--{url}")
        else:
            for i in res_head:
                if yanzheng_url(i):
                    url_temp = i
                    break
    if url_temp:
        return url_temp
    else:
        print('没有可用的地址')


def yanzheng_url(url):
    res = requests.get(url)
    if res.status_code == 200:
        return True
    else:
        return False

if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                 '(KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    headers = {'user-agent': user_agent}
    thread2 = ThreadPoolExecutor(max_workers=30)
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    if not os.path.isdir('pic/'):
        os.mkdir('pic/')
    total_pages = 2
    url_head = url_head_list(headers)
    print(url_head)
    # url_list = ['{}/thread0806.php?fid=16&search=&page={}'.format(url_head, i) for i in range(1, total_pages)]
    # for url in url_list:
    #     # url = url_list[0]
    #     page_adr = parse_1(url)
    #     parse_2(page_adr,  thread2)
    # # for j in ALL_TASK:
    #     # print(j.done())
    # thread2.shutdown(wait=True)









