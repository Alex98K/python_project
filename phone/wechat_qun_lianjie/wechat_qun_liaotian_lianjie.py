# -*- coding: utf-8 -*-
import datetime
import json
import os
import re
import time
import requests
import win32api
import win32clipboard as w
import win32con
import xlwt
from selenium import webdriver
import uiautomator2


def rollback(pp):
    if not pp(resourceId="com.tencent.mm:id/m1").click_exists(timeout=timeout):
        pp.press("back")


def write_json(data):
    with open('all.json', 'w+') as f1:
        json.dump(data, f1, ensure_ascii=False, indent=2)


def json2excel():
    with open("all.json", "r") as f2:
        all_data = json.load(f2)
        # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    # style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold off',
    #                      num_format_str='#,##0.00')
    # style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    # 创建sheet
    data_sheet = workbook.add_sheet('统计')
    row0 = [u'标题', u'发布者', u'发布日期', u'发布渠道', u'网址']
    for i in range(len(row0)):
        data_sheet.write(0, i, row0[i])
    for k, v in enumerate(all_data):
        data_sheet.write(k+1, 0, v)
        data_sheet.write(k+1, 1, all_data[v][0])
        data_sheet.write(k+1, 2, all_data[v][1])
        data_sheet.write(k+1, 3, all_data[v][2])
        data_sheet.write(k+1, 4, all_data[v][3])
    workbook.save('结果.xls')


def main(pp):
    while True:
        for j in pp(resourceId="com.tencent.mm:id/b6"):  # 获取每个发布人的信息
            try:
                auther = j.get_text()  # 获取发布人
                title_temp_uioj = j.down(resourceId="com.tencent.mm:id/bd")  # 标题UI对象
                title_temp = title_temp_uioj.get_text().replace(u'\u200b', u'')\
                    .replace(u'\u3000', u'').replace(u'\xa0', u'')  # 标题
            except Exception as e1:
                print('***获取发布人或者标题错误***', e1)
                continue
            try:
                qudao_temp_uioj = j.down(resourceId="com.tencent.mm:id/b_")  # 发布渠道UI对象
                qudao_temp = qudao_temp_uioj.get_text().replace(u'\u200b', u'')\
                    .replace(u'\u3000', u'').replace(u'\xa0', u'').replace(u'💮', u'').replace(u'🕊', u'')    # 发布渠道
            except Exception as e2:
                print('***获取发布渠道错误***', e2)
                qudao_temp = "发布渠道为空"
            try:
                date_temp_uioj = j.sibling(resourceId="com.tencent.mm:id/bc")  # 获取发布时间UI对象
                date_temp = date_temp_uioj.get_text()  # 获取发布时间
                if date_temp == "今天":
                    date_temp = str(datetime.date.today() - datetime.timedelta(days=0))
                elif date_temp == '昨天':
                    date_temp = str(datetime.date.today() - datetime.timedelta(days=1))
                elif '天前' in date_temp:
                    date_temp = str(datetime.date.today() - datetime.timedelta(days=int(date_temp.replace('天前', ''))+1))
            except Exception as e3:
                print('***获取发布时间错误***', e3)
                date_temp = "发布时间为空"
            p = "网址不存在"
            if title_temp not in title or (title[title_temp][2] != qudao_temp and p != "网址不存在"):
                if not title_temp_uioj.click_gone(maxretry=10, interval=1.0):
                    raise Exception("点击标题，但是进不去网页")
                if not (pp(description="更多").exists(timeout=timeout) and pp(description="更多").click_gone(maxretry=10,
                                                                                                         interval=1.0)):
                    rollback(pp)
                if pp(text="复制链接").exists(timeout=timeout) and pp(text="复制链接").click_gone(maxretry=10, interval=1.0):
                    p = pp.clipboard
                    rollback(pp)
                else:
                    pp(text="取消").click_exists(timeout=timeout)
                    rollback(pp)
                title[title_temp] = [auther, date_temp, qudao_temp, p]
                print(f'标题：{title_temp}\n 发布者：{auther}\n 发布日期：{date_temp}\n 发布渠道：{qudao_temp}\n 网址:{p}')
                write_json(title)
        time.sleep(0.5)
        if not pp(scrollable=True).scroll(100):
            break
        # pp.swipe(0.5, 0.8, 0.5, 0.2, 0.5)


def get_text():  # 读取剪切板
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d


def set_text(string):  # 写入剪切板
    w.OpenClipboard()
    w.EmptyClipboard()
    # w.SetClipboardData(win32con.CF_TEXT, aString)  # 这个中文会有乱码
    w.SetClipboardData(win32con.CF_UNICODETEXT, string)  # 这个中文没有乱码
    w.CloseClipboard()


def save_html(title1, url):
    set_text(re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", str(title1 + ".mhtml")))  # 将“test”写入剪切板
    # 测试网址
    # url1 = "http://news.youth.cn/sz/201812/t20181218_11817816.htm"
    # 打开另存为mhtml功能
    options = webdriver.ChromeOptions()
    options.add_argument('--save-page-as-mhtml')
    # 设置chromedriver，并打开webdriver
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application/chromedriver.exe", chrome_options=options)
    driver.get(url)
    # 有些网站需要点击一下页面，才能进行保存，比如csdn
    # #鼠标移动到某一位置，左键点击一下
    # windll.user32.SetCursorPos(100, 100)#坐标值
    # time.sleep(0.05)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    # # # 模拟键盘操作
    win32api.keybd_event(17, 0, 0, 0)           # 按下ctrl
    # win32api.keybd_event(65, 0, 0, 0)           # 按下a
    # win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放a
    win32api.keybd_event(83, 0, 0, 0)           # 按下s
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放s
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放ctrl
    # #加上休眠时间等待弹框的出现
    time.sleep(2)
    print(get_text())
    # 自动粘贴剪切板中的内容
    win32api.keybd_event(17, 0, 0, 0)  # ctrl的键位码是17
    win32api.keybd_event(86, 0, 0, 0)  # v的键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(13, 0, 0, 0)  # Enter的键位码是13
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(13, 0, 0, 0)           # 按下enter
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放enter
    # #如果文件已存在，会在弹出一个提示框，提示是否要替换，默认是否选项，
    # #按下键盘小箭头左移，选择是，然后再次按下enter，
    time.sleep(2)  # 加上休眠时间等待弹框的出现
    win32api.keybd_event(37, 0, 0, 0)           # 按下小箭头左移
    win32api.keybd_event(37, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放小箭头左移
    time.sleep(0.5)
    win32api.keybd_event(13, 0, 0, 0)           # 按下enter
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放enter
    # 关闭webdriver
    driver.close()


def save_jpg():
    for k, v in title.items():
        if v[-1] != "网址不存在":
            # save_html(k, v[-1])  # 保存每个网页
            k = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", k)
            if not os.path.exists(f'pic/{k}'):  # 判断是否存在文件夹如果不存在则创建为文件夹
                try:
                    urls = re.findall(pattern, requests.get(v[-1]).text)
                except Exception:
                    continue
                if not urls:
                    continue
                os.makedirs(f'pic/{k}')
                try:
                    for i, j in enumerate(urls):
                        jpg = requests.get(j[0]).content
                        with open(f"pic/{k}/{i}.{j[1]}", 'wb') as f:
                            f.write(jpg)
                            print('保存图片')
                except Exception:
                    pass


if __name__ == '__main__':
    timeout = 8
    pattern = r'"(http.*?[\.|=](jpeg|png|jpg|gif))"'
    pp = uiautomator2.connect_usb('8DF6R16729018868')
    # print(pp.dump_hierarchy())
    with open("all.json", "r") as f:
        try:
            title = json.load(f)
    #         # 回到上次保存的新闻链接最后位置,测试效果不好，找不到
    #         # last_title = list(title.keys())[-1]
    #         # print(last_title)
    #         # pp(scrollable=True).scroll.to(text=last_title)
        except Exception as e0:
            print(e0)
            title = {}
    #         # 回到聊天记录开始位置
    #         pp(scrollable=True).scroll.toBeginning(steps=10, max_swipes=1000)
    print(title)
    # main(pp)  # 主程序，开始自动操作保存数据
    json2excel()  # 把保存数据存为EXCEL
    # save_jpg()  # 把每个网页、每页的图片保存下来

