# -*-coding:utf8-*-
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from copy import copy
import requests
from lxml import etree
import socket


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


def page_title_pic_url(index, html_url):
    """
     # 获取列表页的相关内容，以及每个详情页的内容，包括每页图片的地址，形成一个全部信息的字典PAGE_DATA，并且进行文件保存
    :param index: 标题页索引序号
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
    global PAGE_DATA
    try:
        html1 = etree.HTML(download(html_url).text)
    except AttributeError:
        return None
    if not len(html1):
        return None
    # 标题列表
    html_title = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]//h3/a//text()")
    # 详情页地址列表
    pic_url_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]//h3/a/@href")
    # 点赞数列表
    dian_zan_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]/td[1]//text()")
    dian_zan_list = remove_trip_list(dian_zan_list)
    # 作者列表
    author_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]/td[3]/a//text()")
    # 回复数列表
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
    if not page_url:
        return
    print(f'***********第{index+1}页标题页读取完成***********')
    # print(page_url)
    for i, v in enumerate(page_url):
        if condition_title(v[0]) and int(v[2]) >= 0 and int(v[3]) >= 0 and condition_author(v[4]):
            try:
                date_html = etree.HTML(download(url_head + v[1]).text)
                if pic_down_adr_list1 := date_html.xpath("//img/@ess-data"):
                    pic_down_adr_list = pic_down_adr_list1
                elif pic_down_adr_list2 := date_html.xpath("//img/@src"):
                    pic_down_adr_list = pic_down_adr_list2
                else:
                    print(f'获取{v[0]}页的图片地址为空，跳过')
                    continue
            except Exception as e:
                print(e)
                print(f'获取{v[0]}详细页，就是图片页出现错误，跳过')
                continue
            time.sleep(INTERVAL_TIME_DETAIL)
            try:
                post_date = remove_trip_list(date_html.xpath("//div[@class='tipad']/text()"))[0].replace('Posted:', '')
            except IndexError:
                post_date = None
            # print(f'{v[0]} 图片下载地址是', pic_down_adr_list)
            print(f'{v[0]} 图片下载地址获取成功')
            PAGE_DATA[v[0]] = (v[1], v[2], v[3], v[4], post_date, pic_down_adr_list)
            with open(page_data_dir, 'w', encoding='UTF-8') as fp:
                try:
                    json.dump(PAGE_DATA, fp, ensure_ascii=False, indent=2)
                    print('保存page_data文件完成')
                except UnicodeEncodeError:
                    print("出现UnicodeEncodeError编码错误，跳过保存该页面信息")


def page_down(pic_dir_adr, thread):
    """
    下载PAGE_DATA中图片的函数
    :param pic_dir_adr:pic文件夹路径，用来计算下面文件夹目录地址
    :param thread: 线程对象
    :return:
    """
    def down_one_pic(dir_path_c, url_one1, pic_name, index1, file_name1):
        """
         # 下载一个图片
        :param dir_path_c: 文件夹路径
        :param file_name1:文件名
        :param url_one1: 图片地址
        :param pic_name:图片名字
        :param index1:图片索引排序
        """
        if len(pic_data := download(url_one1).content) > 1000:
            print('下载完一个图片 {}-{}'.format(pic_name, index1))
            if not os.path.exists(dir_path_c):
                try:
                    os.makedirs(dir_path_c)
                except OSError:
                    print(f"创建下载图片目录文件夹{dir_path_c}出错")
                    return
            with open(file_name1, 'wb') as f11:
                f11.write(pic_data)

    def condition_title(title):  # 标题不能包含什么或者必须包含什么才能下载
        title_pass_down_list = []  # 计划下载的标题中不应该包含的关键字列表
        title_keep_down_word = ''  # 计划下载的标题中必须包含的关键字
        if list(filter(lambda x: x in str(title), title_pass_down_list)):
            return False
        elif title_keep_down_word not in str(title):
            return False
        else:
            return True

    def condition_author(author):  # 作者是谁或者不能是谁，才下载
        author_pass_down_list = []
        author_keep_down_word = ''
        if str(author) not in author_pass_down_list:
            if len(author_keep_down_word) > 0 and author_keep_down_word in str(author):
                return True
            elif len(author_keep_down_word) == 0:
                return True
            else:
                return False
        else:
            return False

    def dian_zan(num):  # 点赞大于一定条件才下载
        dian_zan_hum = 0
        if int(num) >= dian_zan_hum:
            return True
        else:
            return False

    def hui_fu(num):  # 回复大于一定条件才下载
        hui_fu_num = 0
        if int(num) >= hui_fu_num:
            return True
        else:
            return False

    for key, val in PAGE_DATA.items():
        if condition_title(val[0]) and dian_zan(val[1]) and hui_fu(val[2]) and condition_author(val[3]):
            dir_name = f'点赞：{val[1]} ' + '--' + f'回复：{val[2]} ' + '--' + f'标题：{key}' + '--' + f'作者：{val[3]}'
            dir_path = os.path.join(pic_dir_adr, dir_name)
            for index, pic_url_one in enumerate(val[5]):
                try:
                    suffix = re.search(r'\.\w*$', pic_url_one).group()
                except AttributeError:
                    suffix = '.jpg'
                file_name = os.path.join(dir_path, '{}-{}{}'.format(key, index, suffix))
                if not os.path.exists(file_name):
                    time.sleep(INTERVAL_TIME_PIC)
                    thread.submit(down_one_pic, dir_path, pic_url_one, key, index, file_name)
                    if INTERVAL_TIME_PIC >= 1 and WORKER_NUM_PIC <= 5:
                        print("提交一个线程, {}-{}".format(key, index))
                        pass


def url_head_new(headers2):
    """
    用来获取新的1024地址，从rr567网站点击两次可以获取到。
    :param headers2:通用请求头
    :return:获取到的地址
    """
    url_start = 'https://rr567.net/'
    headers2['cookie'] = '__cfduid=d8820278eebccdea98714721a2976fa7b1569319655; _ga=GA1.2.829357220.1569319655; ' \
                         'page=http%3A%2F%2Frvedc.com; _gid=GA1.2.334072831.1590379178; fuck1=yes '
    print("准备获取新地址")
    res = requests.get(url_start, headers=headers1, timeout=30).text
    try:
        head = re.search(r"href='h.*?'", res).group()[6:-1]
        print("获取新地址成功")
        return head
    except TypeError:
        print('在首页获取1024网址出错')
    except AttributeError:
        print('在首页获取1024网址出错')


def store_return_url(url2=None, headers_ve=None):
    """
    将新获取的地址传入，进行验证，如果可以用，就加入原来的json中存储，如果不可用，就用原来的json中遍历获取一个可以用的地址
    :param headers_ve:请求头
    :param url2:新获取的地址
    :return:可用的1024地址
    """
    url_temp = None
    sign = 0
    with open(url_head_dir, 'r', encoding='UTF-8') as f3:
        try:
            head_list = json.load(f3)
        except json.decoder.JSONDecodeError:
            head_list = []
        if verify_url(url2, host=url2[8:-10], headers_ver=headers_ve):
            print(f"新获取的地址可以使用：{url2}")
            url_temp = url2
            if url2 not in head_list:
                head_list.append(url2)
                sign = 1
        else:
            print('新地址不可使用，从存储的地址中获取')
            for i in head_list:
                print(f'测试地址： {i}')
                if verify_url(i, host=i[8:-10], headers_ver=headers_ve):
                    url_temp = i
                    break
    if sign == 1:
        with open(url_head_dir, 'w', encoding='UTF-8') as f2:
            json.dump(head_list, f2)
            print(f"加入新地址--{url2}")
    if url_temp:
        return url_temp
    else:
        print('没有可用的URL地址')
        return None


def store_return_ip(headers_ver):
    def run(headers_v):
        for k in head_list:
            print(f'获取{k}的IP地址')
            my_addr = socket.getaddrinfo(host=k[8:-10], port=80, family=socket.AF_INET)
            if my_addr:
                for j in my_addr:
                    if verify_url(k[0:4] + k[5:8] + j[4][0] + k[-10:], host=k[8:-10], headers_ver=headers_v):
                        url_t = k[0:4] + k[5:8] + j[4][0] + k[-10:]
                        return url_t
    with open(url_head_dir, 'r', encoding='UTF-8') as f3:
        try:
            head_list = json.load(f3)
        except json.decoder.JSONDecodeError:
            head_list = []
        url_temp = run(headers_ver)
    if url_temp:
        return url_temp
    else:
        print('没有可用的IP地址')
        return None


def verify_url(url3, host, headers_ver):
    """
    用来验证获取的1024地址是否可用
    :param headers_ver:请求头
    :param host: 请求头host字段
    :param url3:地址
    :return:是否可用
    """
    headers_ver['Host'] = host
    try:
        res = requests.get(url3, headers=headers_ver, timeout=3)
    except Exception as e:
        print(f'验证地址{url3}出现错误', e)
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
    total_pages = 5  # 计划获取多少个标题页的信息，如果以前page_data.json没有存储，可设为100，如果存储过，依据更新频率确定。
    INTERVAL_TIME_PIC = 0  # 下载图片的请求间隔时间，太短容易被图片所在网站禁IP或者封UA
    INTERVAL_TIME_DETAIL = 0.1  # 详情页请求间隔时间，太短容易被1024网站禁IP
    WORKER_NUM_PIC = 60  # 下载图片时候的线程数
    WORKER_NUM_PAGE = 1  # 下载页面时候的线程数
    # 请求头信息，用于下载器的get请求
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/83.0.4103.116 Safari/537.36 '
    headers = {'user-agent': user_agent}
    headers1 = {'user-agent': user_agent}
    PATH = os.path.abspath(os.path.dirname(__file__))
    pic_dir = os.path.join(PATH, 'pic')
    url_head_dir = os.path.join(PATH, 'url_head.json')
    page_data_dir = os.path.join(PATH, 'page_data.json')
    if not os.path.isdir(pic_dir):
        os.mkdir(pic_dir)
    # 下面的代码是为了删除文件夹中大小小于1000字节的文件，一般为下载出现错误保存的文件，同时删除空文件夹
    for root1, dirs, files1 in os.walk(pic_dir):
        for file1 in files1:
            if os.stat(del_path := os.path.join(root1, file1)).st_size < 1000:
                print(del_path)
                os.remove(del_path)
        for dir_one in dirs:
            try:
                os.rmdir(os.path.join(root1, dir_one))
            except OSError:
                pass
    # 下面的是获取page_data中保存的之前的标题、图片信息，存入PAGE_DATA字典中
    try:
        with open(page_data_dir, 'r', encoding='UTF-8') as f1:
            try:
                PAGE_DATA = json.load(f1)
            except json.decoder.JSONDecodeError:
                PAGE_DATA = {}
    except FileNotFoundError:
        with open(page_data_dir, 'w', encoding='UTF-8') as f12:
            json.dump({}, f12)
            PAGE_DATA = {}
    # 获取可用的1024网站域名，如果不成功，尝试获取可用的直连IP地址
    if url_head := store_return_url(url_head_new(headers1), headers_ve=headers1):
        pass
    else:
        url_head = store_return_ip(headers_ver=headers1)
    thread1 = ThreadPoolExecutor(max_workers=WORKER_NUM_PAGE)
    if url_head:  # 有网址、有域名，才能下载标题页，否则就用存储的信息下载图片
        url_head = url_head[:-9]
        url_list = ['{}thread0806.php?fid=16&search=&page={}'.format(url_head, i) for i in range(1, total_pages+1)]
        for url_index, url_one in enumerate(url_list):
            thread1.submit(page_title_pic_url, url_index, url_one)
    else:
        print('没有可用网址，可能被禁IP了，跳过网站获取详细页信息，直接从原来存储的page_data中获取地址，下载图片')
    thread1.shutdown(wait=True)
    for n in range(5):
        thread2 = ThreadPoolExecutor(max_workers=WORKER_NUM_PIC)
        page_down(pic_dir, thread2)
        thread2.shutdown(wait=True)
