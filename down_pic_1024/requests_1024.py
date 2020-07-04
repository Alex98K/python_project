# -*-coding:utf8-*-
import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from copy import copy
import requests
from lxml import etree


# 每个详细页面名字的xpath地址     '//td[contains(@class,'tal')]/h3/a/font/text()'
# 每个详细页面的xpath地址    '//td[contains(@class,'tal')]/h3/a/@href'
# 图片xpath地址     '//img/@src'


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


def page_title_pic_url(html_url):
    """
     # 获取列表页的相关内容，以及每个详情页的内容，包括每页图片的地址，形成一个全部信息的字典PAGE_DATA，并且进行文件保存
    :param html_url:列表页地址
    """
    def condition_title(title, update: bool = False):
        if list(filter(lambda x: x in title, PASS_TITLE)):
            return False
        elif (title in PAGE_DATA.keys()) and not update:
            return False
        else:
            return True

    def condition_author(author):
        author_pass_list = []
        if author not in author_pass_list:
            return True
        else:
            return False

    def remove_trip_list(list2):  # 去除列表中的空字符/r /n /t 等，返回去除后的列表副本
        list1 = copy(list2)
        for i1, j in enumerate(list1):
            list1[i1] = list1[i1].strip()
            if '.::' in j:
                list1[i1] = '0'
        while list1.count(''):
            list1.remove('')
        return list1

    html1 = etree.HTML(download(html_url).text)
    html_title = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]//h3/a//text()")
    pic_url_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]//h3/a/@href")
    dian_zan_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]/td[1]//text()")
    dian_zan_list = remove_trip_list(dian_zan_list)
    author_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]/td[3]/a//text()")
    hui_fu_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]/td[4]//text()")
    hui_fu_list = remove_trip_list(hui_fu_list)
    if len(html_title) != len(pic_url_list):
        print(f"详细页标题数{len(html_title)}和地址数{len(pic_url_list)}不一致")
        raise
    if len(html_title) != len(dian_zan_list):
        print(f"详细页标题数{len(html_title)}和点赞数{len(dian_zan_list)}不一致")
        raise
    if len(html_title) != len(author_list):
        print(f"详细页标题数{len(html_title)}和发布者数{len(author_list)}不一致")
        raise
    if len(html_title) != len(hui_fu_list):
        print(f"详细页标题数{len(html_title)}和回复数{len(hui_fu_list)}不一致")
        raise
    for i, k in enumerate(html_title):
        html_title[i] = re.sub(r"[/\\:*?\"<>|]", "", k)
    page_url = list(zip(html_title, pic_url_list, dian_zan_list, hui_fu_list, author_list))
    print(page_url)
    for i, v in enumerate(page_url):
        if condition_title(v[0]) and int(v[2]) >= 0 and int(v[3]) >= 0 and condition_author(v[4]):
            try:
                date_html = etree.HTML(download(url_head + v[1]).text)
                pic_down_adr_list = date_html.xpath("//img/@ess-data")
                time.sleep(INTERVAL_TIME_DETAIL)
            except Exception as e:
                print(e)
                print(f'获取{v[0]}详细页，就是图片页出现错误，跳过')
                continue
            try:
                post_date = remove_trip_list(date_html.xpath("//div[@class='tipad']/text()"))[0].replace('Posted:', '')
            except IndexError:
                post_date = None
            print(f'{v[0]} 图片下载地址是', pic_down_adr_list)
            PAGE_DATA[v[0]] = (v[1], v[2], v[3], v[4], post_date, pic_down_adr_list)
            with open('page_data.json', 'w', encoding='UTF-8') as fp:
                try:
                    json.dump(PAGE_DATA, fp, ensure_ascii=False, indent=2)
                    print('保存page_data文件完成')
                except UnicodeEncodeError:
                    print("出现UnicodeEncodeError编码错误，跳过保存该页面信息")


def page_down(pic_dir_adr, thread1):
    """
    下载PAGE_DATA中图片的函数
    :param pic_dir_adr:pic文件夹路径，用来计算下面文件夹目录地址
    :param thread1: 线程对象
    :return:
    """
    def down_one_pic(url_one1, pic_name, index1, file_name1):
        """
         # 下载一个图片
        :param file_name1:
        :param url_one1: 图片地址
        :param pic_name:图片名字
        :param index1:图片索引排序
        """
        if pic_data := download(url_one1).content:
            print('下载完一个图片 {}-{}'.format(pic_name, index1))
            with open(file_name1, 'wb') as f11:
                f11.write(pic_data)

    for key, val in PAGE_DATA.items():
        dir_name = key + '--' + f'点赞数{val[1]}' + '--' + f'回复数{val[2]}' + '--' + f'作者是{val[3]}'
        dir_path = os.path.join(pic_dir_adr, dir_name)
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except OSError:
                print(f"创建下载图片目录文件夹{dir_path}出错")
                continue
        for index, pic_url_one in enumerate(val[5]):
            suffix = re.search(r'\.\w*$', pic_url_one).group()
            file_name = os.path.join(dir_path, '{}-{}{}'.format(key, index, suffix))
            if not os.path.exists(file_name):
                time.sleep(INTERVAL_TIME)
                task = thread1.submit(down_one_pic, pic_url_one, key, index, file_name)
                print("{}提交一个线程, {}-{}".format(threading.current_thread().name, key, index))
                task.running()


def url_head_new(headers1):
    """
    用来获取新的1024地址，从rr567网站点击两次可以获取到。
    :param headers1:通用请求头
    :return:获取到的地址
    """
    url_start = 'https://rr567.net/'
    headers1['cookie'] = '__cfduid=d8820278eebccdea98714721a2976fa7b1569319655; _ga=GA1.2.829357220.1569319655; ' \
                         'page=http%3A%2F%2Frvedc.com; _gid=GA1.2.334072831.1590379178; fuck1=yes '
    print("准备获取新地址")
    res = requests.get(url_start, headers=headers1, timeout=30).text
    try:
        head = re.search(r"href='h.*?'", res).group()[6:-1]
        print("获取新地址成功")
        return head
    except TypeError:
        print('在首页获取1024网址出错')


def store_return_url(url2=None):
    """
    将新获取的地址传入，进行验证，如果可以用，就加入原来的json中存储，如果不可用，就用原来的json中遍历获取一个可以用的地址
    :param url2:新获取的地址
    :return:可用的1024地址
    """
    url_temp = None
    sign = 0
    with open('url_head.json', 'r', encoding='UTF-8') as f3:
        try:
            head_list = json.load(f3)
        except json.decoder.JSONDecodeError:
            head_list = []
        if verify_url(url2):
            print(f"新获取的地址可以使用：{url2}")
            url_temp = url2
            if url2 not in head_list:
                head_list.append(url2)
                sign = 1
        else:
            print('新地址不可使用，从存储的地址中获取')
            for i in head_list:
                print(f'测试地址{i}')
                if verify_url(i):
                    url_temp = i
                    break
    if sign == 1:
        with open('url_head.json', 'w', encoding='UTF-8') as f2:
            json.dump(head_list, f2)
            print(f"加入新地址--{url2}")
    if url_temp:
        return url_temp
    else:
        print('没有可用的地址')
        return None


def verify_url(url3):
    """
    用来验证获取的1024地址是否可用
    :param url3:地址
    :return:是否可用
    """
    try:
        res = requests.get(url3, timeout=3)
    except requests.exceptions.ReadTimeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    if res.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    # 标题中不得含有的关键词列表，如果有列表中的关键词，会屏蔽下载及获取信息，节省资源
    PASS_TITLE = ['上传图片发布', '各类图片上传的图床',
                  '自拍区发帖前必读', '新手必學', '官方客戶',
                  '为什么你的帖子没有得到评分', '图区禁止使用下列图床', '發圖貼會員&訪客須知']
    total_pages = 100  # 计划获取多少个标题页
    INTERVAL_TIME = 0  # 下载图片的请求间隔时间，太短容易被禁IP
    INTERVAL_TIME_DETAIL = 10  # 详情页请求间隔时间，太短容易被禁IP
    WORKER_NUM = 100  # 下载图片时候的线程数
    # 请求头信息，用于下载器的get请求
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                 '(KHTML, like Gecko) Chrome/80.0.3945.88 Safari/537.36'
    headers = {'user-agent': user_agent}
    PATH = os.path.abspath(os.path.dirname(__file__))
    pic_dir = os.path.join(PATH, 'pic')
    if not os.path.isdir(pic_dir):
        os.mkdir(pic_dir)
    try:
        with open('page_data.json', 'r', encoding='UTF-8') as f1:
            try:
                PAGE_DATA = json.load(f1)
            except json.decoder.JSONDecodeError:
                PAGE_DATA = {}
    except FileNotFoundError:
        with open('page_data.json', 'w', encoding='UTF-8') as f12:
            json.dump({}, f12)
            PAGE_DATA = {}
    url_head = store_return_url(url_head_new(headers))
    if url_head:
        url_head = store_return_url(url_head_new(headers))[:-9]
        url_list = ['{}thread0806.php?fid=16&search=&page={}'.format(url_head, i) for i in range(1, total_pages+1)]
        print(url_list)
        for url_one in url_list:
            page_title_pic_url(url_one)
    else:
        print('没有可用网址，可能被禁IP了，跳过网站获取详细页信息，直接从原来存储的page_data中获取地址，下载图片')
    thread = ThreadPoolExecutor(max_workers=WORKER_NUM)
    page_down(pic_dir, thread)
    thread.shutdown(wait=True)
