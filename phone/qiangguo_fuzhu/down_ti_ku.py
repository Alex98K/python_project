import json
import os
import re
import requests
from lxml import etree


def fix_answer(answer_list, answer_num):
    res_li = []
    for j in answer_list:
        if '.' not in j:
            res_li[-1] = res_li[-1] + j
        else:
            res_li.append(re.sub(r'^\d{0,2}\.', '', j))
    if len(res_li) != answer_num:
        print(f'应该有10个答案的，但是获取的有{len(res_li)}个，请查错')
        raise
    return res_li


def get_url_ti(urls, ti_all):
    url = urls[0]
    answer_num = urls[1]
    try:
        ti_url_1 = requests.get(url, timeout=5)
        ti_url_1.encoding = "utf-8"
    except Exception as e:
        print(e)
        return {}
    ti_ku = {}
    try:
        temp = etree.HTML(ti_url_1.text).xpath('//div[@class="post-page-wrapper-content"]//h4')
    except Exception as e:
        print(e)
        return {}
    for i in temp:
        title = list(map(lambda t: re.sub(r'[^\w\u4e00-\u9fa5]', '', str(t).replace('\xa0', '').replace('_', '')),
                         i.xpath('.//text()')))[0]
        title = re.sub(r'第\d{0,4}期', '', title)
        if title in ti_all.keys():
            continue
        answer = list(map(lambda t: re.sub(r'[^\w\u4e00-\u9fa5.]', '', str(t).replace('\xa0', '').replace('_', '')),
                          i.xpath(f'./following-sibling::p[position()<{answer_num+2}]/text()')))
        # print(title)
        answer = fix_answer(answer, answer_num)
        # print(answer)
        ti_ku[title] = answer
    return ti_ku


def down_ti():
    path = os.path.abspath(os.path.dirname(__file__))
    try:
        with open(os.path.join(path, f'zhuan_xiang.json'), 'r', encoding="UTF-8") as f1:
            special_ti_all = json.load(f1)
    except FileNotFoundError:
        special_ti_all = {}
    try:
        with open(os.path.join(path, f'mei_zhou.json'), 'r', encoding="UTF-8") as f2:
            week_ti_all = json.load(f2)
    except FileNotFoundError:
        week_ti_all = {}
    special_url_list = [
        ['https://124731.cn/post/390.html', 10],
        ['https://124731.cn/post/392.html', 10],
        ['https://124731.cn/post/395.html', 10],
    ]
    week_url_list = [
        ['https://124731.cn/post/391.html', 5],
        ['https://124731.cn/post/394.html', 5],
        ['https://124731.cn/post/393.html', 5],
    ]
    for j_special in special_url_list:
        special = get_url_ti(j_special, special_ti_all)
        if not special:
            continue
        else:
            special_ti_all = dict(special_ti_all, **special)
    if special_ti_all:
        with open(f'zhuan_xiang.json', 'w', encoding='UTF-8') as f2:
            json.dump(special_ti_all, f2, ensure_ascii=False, indent=2)
    for j_week in week_url_list:
        week = get_url_ti(j_week, week_ti_all)
        if not week:
            continue
        else:
            week_ti_all = dict(week_ti_all, **week)
    if week_ti_all:
        with open(f'mei_zhou.json', 'w', encoding='UTF-8') as f2:
            json.dump(week_ti_all, f2, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    down_ti()
