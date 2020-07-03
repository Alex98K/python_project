# -*-coding:utf8-*-
from copy import copy

from lxml import etree
import requests
import os, shutil, threading, re, time, json
from concurrent.futures import ThreadPoolExecutor


# 每个详细页面名字的xpath地址     '//td[contains(@class,'tal')]/h3/a/font/text()'
# 每个详细页面的xpath地址    '//td[contains(@class,'tal')]/h3/a/@href'
# 图片xpath地址     '//img/@src'


def download(url):  # 下载器，将传入的url地址进行get请求，获取返回页面
    try:
        response = requests.get(url=url, headers=headers, timeout=100)
        response.keep_alive = False
        response.encoding = 'gbk'
        if response.status_code != 200:
            print(f'这个地址的网页获取失败--{url}')
        return response
    except Exception as e:
        print(e, url)


def remove_trip_list(list2):  # 去除列表中的空字符/r /n /t 等，返回去除后的列表副本
    list1 = copy(list2)
    for i, j in enumerate(list1):
        list1[i] = list1[i].strip()
        if '.::' in j:
            list1[i] = '0'
    while list1.count(''):
        list1.remove('')
    return list1


def page_title_url(url):
    """
     # 获取列表页的相关内容，也就是盖区的标题列表页
    :param url:列表页地址
    :return:列表，包含标题，地址,点赞数、回复数、作者
    """
    html1 = etree.HTML(res := download(url).text)
    # print(res)
    html_title = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]//h3/a//text()")
    pic_url_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]//h3/a/@href")
    dian_zan_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]/td[1]//text()")
    dian_zan_list = remove_trip_list(dian_zan_list)
    auther_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]/td[3]/a//text()")
    hui_fu_list = html1.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]/td[4]//text()")
    hui_fu_list = remove_trip_list(hui_fu_list)
    if len(html_title) != len(pic_url_list):
        print(f"详细页标题数{len(html_title)}和地址数{len(pic_url_list)}不一致")
        raise
    if len(html_title) != len(dian_zan_list):
        print(f"详细页标题数{len(html_title)}和点赞数{len(dian_zan_list)}不一致")
        raise
    if len(html_title) != len(auther_list):
        print(f"详细页标题数{len(html_title)}和发布者数{len(auther_list)}不一致")
        raise
    if len(html_title) != len(hui_fu_list):
        print(f"详细页标题数{len(html_title)}和回复数{len(hui_fu_list)}不一致")
        raise
    # html_url = map(lambda x: url_head + x, pic_url_list)
    # return list(zip(html_title, html_url, dian_zan_list, hui_fu_list, auther_list))
    return list(zip(html_title, pic_url_list, dian_zan_list, hui_fu_list, auther_list))


def down_one_pic(url_one, dir_path, pic_name, index):
    """
     # 下载一个图片
    :param url_one: 图片地址
    :param dir_path:存储路径
    :param pic_name:图片名字
    :param index:图片索引排序
    :return:
    """
    style = re.search(r'\.\w*$', url_one).group()
    file_name = os.path.join(dir_path, '{}-{}{}'.format(pic_name, index, style))
    if (not os.path.exists(file_name)) and (pic_data := download(url_one).content):
        print('下载完一个图片 {}-{}'.format(pic_name, index))
        with open(file_name, 'wb') as f:
            f.write(pic_data)


def detail_page_down(page_adr, thread2):
    def tiaojian_title(title):
        if title in PASS_TITLE or '官方客戶端' in title or '新手必學' in title:
            return False
        else:
            return True

    def tiaojian_dianzan(dianzan):
        if int(dianzan) >= 0:
            return True
        else:
            return False

    def tiaojian_huifu(huifu):
        if int(huifu) >= 0:
            return True
        else:
            return False

    def tiaojian_auther(auther):
        # auther_list = []
        # if auther in auther_list:
        #     return True
        # else:
        #     return False
        return True

    def doing():
        if tiaojian_title(v[0]) and tiaojian_dianzan(v[2]) and tiaojian_huifu(v[3]) and tiaojian_auther(v[4]) and \
                (pic_down_adr_list := (date_html := etree.HTML(download(url_head + v[1]).text)).xpath("//img/@ess-data")):
            post_date = remove_trip_list(date_html.xpath("//div[@class='tipad']/text()"))[0]
            print(f'{v[0]} 图片下载地址是', pic_down_adr_list)
            # name = re.sub(rstr, "", v[0]) + '--' + f'点赞数{v[2]}' + '--' + f'回复数{v[3]}' + '--' + f'作者是{v[4]}'
            name = re.sub(rstr, "", v[0]) + '--' + f'作者是{v[4]}'
            pic_dir = os.path.join(path, 'pic')
            if not os.path.isdir(pic_dir):
                os.mkdir(pic_dir)
            dir_path = os.path.join(pic_dir, name)
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                except OSError:
                    raise
                finally:
                    for index, pic_url_one in enumerate(pic_down_adr_list):
                        time.sleep(1)
                        task = thread2.submit(down_one_pic, pic_url_one, dir_path, name, index)
                        ALL_TASK.append(task)
                        print("{}提交一个线程, {}-{}".format(threading.current_thread().name, name, index))
                        task.running()
                    print(len(ALL_TASK))
    for i, v in enumerate(page_adr):
        doing()


def url_head_new(headers):
    """
    用来获取新的1024地址，从rr567网站点击两次可以获取到。
    :param headers:通用请求头
    :return:获取到的地址
    """
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
    """
    将新获取的地址传入，进行验证，如果可以用，就加入原来的json中存储，如果不可用，就用原来的json中遍历获取一个可以用的地址
    :param url:新获取的地址
    :return:可用的1024地址
    """
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
        raise


def yanzheng_url(url):
    """
    用来验证获取的1024地址是否可用
    :param url:地址
    :return:是否可用
    """
    try:
        res = requests.get(url, timeout=3)
    except requests.exceptions.ReadTimeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    if res.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    ALL_TASK = []
    PASS_TITLE = ['[岛叔原创]怎么上传图片发布在论坛共享的简单图文教程', '各类图片上传的图床[更新7-28]', '自拍区发帖前必读(最新版）', '[技术贴]再现(寡人教程)之发图详解, 其實发图很簡單, 新手必學!', '为什么你的帖子没有得到评分？', '图区禁止使用下列图床，违者永久禁言，屏蔽IP', '發圖貼會員&訪客須知']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                 '(KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    headers = {'user-agent': user_agent}
    path = os.path.abspath(os.path.dirname(__file__))
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
        detail_page_down(page_adr, thread2)
    # for j in ALL_TASK:
        # print(j.done())
    thread2.shutdown(wait=True)









