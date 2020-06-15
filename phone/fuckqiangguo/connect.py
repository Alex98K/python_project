import uiautomator2
from fuzzywuzzy import fuzz, process
import json, codecs
import time


def connect():
    """
    链接手机
    :return: 手机连接指引
    """
    laopo = '3EP7N18C11002513'
    wode = '8DF6R16729018868'
    jiude = 'F7R0214305002612'
    pingban = '0071ea56'
    try:
        pp = uiautomator2.connect_usb(laopo)
        seial = laopo
    except Exception:
        try:
            pp = uiautomator2.connect_usb(wode)
            seial = wode
        except Exception :
            try:
                pp = uiautomator2.connect_usb(pingban)
                seial = pingban
            except Exception:
                try:
                    pp = uiautomator2.connect_usb(jiude)
                    seial = jiude
                except Exception as e:
                    raise e
    return pp


def tiaozhan_title(pp):
    """
    寻找界面中的题目和备选答案
    :param pp: 手机链接指引
    :return:找到的问题，找到的备选答案，每个备选答案的界面坐标
    """
    question = None
    answer = []
    answer_index = []
    for j in pp.xpath('//android.view.View[@index="0"]').all():
        if j.attrib['content-desc'] != '' and j.attrib['content-desc'] != "":
            question = j.attrib['content-desc']
            break
    for j in pp.xpath('//android.view.View[@index="1"]').all():
        if j.attrib['content-desc'] != '' and j.attrib['content-desc'] != "":
            if "历史最高答对" in j.attrib['content-desc']:
                break
            answer.append(j.attrib['content-desc'])
            answer_index.append(j.center())
    if question and answer:
        return question, answer, answer_index


def re_start(pp):
    """
    重新开始
    :param pp:手机连接
    :return:
    """
    for j in pp.xpath('//android.view.View[@index="0"]').all():
        if j.attrib['content-desc'] == "本月":
            pp.press("back")
            time.sleep(1)
    for j in pp.xpath('//android.view.View[@index="1"]').all():
        if j.attrib['content-desc'] == "结束本局":
            pp.click(*j.center())
            time.sleep(1)
    for j in pp.xpath('//android.view.View[@index="7"]').all():
        if j.attrib['content-desc'] == "挑战答题":
            pp.click(*j.center())
            time.sleep(1)
    for j in pp.xpath('//android.view.View[@index="0"]').all():
        if j.attrib['content-desc'] == "再来一局":
            pp.click(*j.center())
            time.sleep(1)
    pass


def dati_click(pp, question, answer, answer_index):
    """
    在题库中找到正确答案，与界面中的答案进行模糊匹配，然后点击答题
    :param pp:手机连接指引
    :param question:找到的问题，
    :param answer:找到的备选答案，
    :param answer_index:每个备选答案的界面坐标
    :return:
    """
    all_tiaozhan = json.load(codecs.open('data.json', 'r', 'utf-8-sig'))
    all_title = []
    all_answer = []
    for i in range(len(all_tiaozhan)):
        all_title.append(all_tiaozhan[i]["title"])
        all_answer.append(all_tiaozhan[i]["answer"])
    find_title = process.extractOne(question, all_title)
    print("匹配出来的题目是", find_title[0])
    find_answer_number = all_title.index(find_title[0])
    answer_res = process.extractOne(all_answer[find_answer_number], answer)
    print("匹配后的最终答案是", answer_res[0])
    answer_index_res = answer.index(answer_res[0])
    pp.click(*answer_index[answer_index_res])


if __name__ == '__main__':
    pp = connect()
    xml = pp.dump_hierarchy()
    print(xml)
    last = None
    xuhao = 0
    while True:
        re_start(pp)
        try:
            question, answer, answer_index = tiaozhan_title(pp)
        except Exception:
            continue
        if question == last:
            continue
        else:
            xuhao += 1
            print("第{}个题目找到的问题是  {}".format(xuhao, question))
            print("第{}个题目包含的答案是  {}".format(xuhao, answer))
            print("第{}个题目答案的坐标分别是  {}".format(xuhao, answer_index))
            last = question
            dati_click(pp, question, answer, answer_index)
        time.sleep(1)

