import json
import re
import requests
from lxml import etree


zhuanxiang_url = 'https://124731.cn/post/390.html'
meizhou_url = 'https://124731.cn/post/391.html'
ti_url_1 = requests.get('http://www.syiban.com/sou/')
ti_url_1.encoding = "utf-8"
ti = etree.HTML(ti_url_1.text).xpath('/html/body/div/div/div[2]/div/div/div/script/text()')
data = re.search(r'ti=".*?"', ti[0]).group()
str_a = data[4:-2]
res = re.findall(r'(.*?)\|\|', str_a)
ti_ku = []
for j in res:
    all1 = re.findall(r'#(.*?)#', j)
    all1[0] = str(all1[0]).replace('\xa0', '').replace('_', '')
    all1[0] = re.sub(r'[^\w\u4e00-\u9fa5]', '', all1[0])
    all1[0] = re.sub(r'出题', '', all1[0])
    all1[0] = re.sub(r'推荐', '', all1[0])
    all1[0] = re.sub(r'\(.*?\)', '', all1[0])
    hah = re.findall(r'[^|]+', re.findall(r'#(.*?\|*.*?)#', j[1:])[0])
    ti_ku.append([all1[0], hah, all1[1]])
with open('ti_ku.json', 'w', encoding='UTF-8') as f2:
    json.dump(ti_ku, f2, ensure_ascii=False, indent=2)
for k in ti_ku:
    if len(k[1]) > 4:
        print(k)
