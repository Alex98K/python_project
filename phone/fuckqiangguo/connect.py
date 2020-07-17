import json
import os
import random
import re
import time

import uiautomator2


def connect():
    """
    链接手机
    :return: 手机连接引用
    """
    lao_po = '3EP7N18C11002513'
    wo_de = '8DF6R16729018868'
    jiu_de = 'F7R0214305002612'
    ping_ban = '0071ea56'
    phone = None
    try:
        phone = uiautomator2.connect_usb(lao_po)
    except Exception as e:
        print(e)
        pass
    try:
        phone = uiautomator2.connect_usb(wo_de)
    except Exception as e:
        print(e)
        pass
    try:
        phone = uiautomator2.connect_usb(ping_ban)
    except Exception as e:
        print(e)
        pass
    try:
        phone = uiautomator2.connect_usb(jiu_de)
    except Exception as e:
        print(e)
        pass
    # try:
    #     phone = uiautomator2.connect_wifi('192.168.1.218')
    # except Exception:
    #     pass
    if phone:
        return phone
    else:
        return False


def do_tiao_zhan_ti(data_ti_ku, duplicate_title):
    if pp(text="结束本局").exists:
        pp(text="结束本局").click()
        time.sleep(1)
        pp(text='再来一局').wait()
        time.sleep(1)
        pp(text='再来一局').click()
    if pp(text="再来一局").exists:
        pp(text='再来一局').click()
    if pp(text="选择联系人").exists:
        pp(description="返回").click()
    pp.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View['
             '1]/android.view.View[1]/android.view.View[1]').wait()
    title = pp.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View['
                     '1]/android.view.View[2]/android.view.View[1]/android.view.View[1]').get_text()
    title = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(title).replace('\xa0', '').replace('_', ''))
    answer = [ans.text for ans in pp.xpath('//android.widget.ListView//android.view.View/android.view.View/android'
                                           '.view.View').all()]
    fuz_title = None
    fuz_choose = None
    fuz_answer_num = None
    fuz_index = None
    for index, num in enumerate(data_ti_ku):
        if title in duplicate_title and title == num[0] and answer == num[1]:
            fuz_index = index
            fuz_title = num[0]
            fuz_choose = num[1]
            fuz_answer_num = num[2]
            break
        elif title not in duplicate_title and title == num[0]:
            fuz_index = index
            fuz_title = num[0]
            fuz_choose = num[1]
            fuz_answer_num = num[2]
            break
    new_title_sign = 0
    if fuz_title is None:  # 没有匹配到
        print('*****没有匹配到题目', title, answer, '记录下来，答案预先设为ABCD')
        data_ti_ku.append([title, answer, 'ABCD'])
        with open('ti_ku_verify.json', 'w', encoding='UTF-8') as f2:
            json.dump(data_ti_ku, f2, ensure_ascii=False, indent=2)
    elif fuz_choose != answer:  # 找到了和原来题目一样，但是选项不一样的题
        print(f'*****找到题目和存储的一样***{title}-{fuz_title}***，但是选项{fuz_choose}-{answer}不一样')
        data_ti_ku.append([title, answer, 'ABCD'])
        duplicate_title = list(set(duplicate_title.append(fuz_title)))
        with open('ti_ku_verify.json', 'w', encoding='UTF-8') as f2:
            json.dump(data_ti_ku, f2, ensure_ascii=False, indent=2)
    else:  # 匹配到了
        # print('匹配到了', fuz_title, answer, '匹配的答案是', fuz_answer_num)
        if len(fuz_answer_num) > 1:
            new_title_sign = 1
            duplicate_title = list(set(duplicate_title.append(fuz_title)))
            print('新加入的题匹配到了', fuz_title, answer, '匹配的答案是', fuz_answer_num)
        if 'A' in fuz_answer_num:
            pp.xpath('//android.widget.ListView//android.view.View/android.view.View/android.view.View').all()[0] \
                .click()
            time.sleep(3)
            if pp(text="结束本局").exists or pp(text="再来一局").exists:
                fuz_answer_num = fuz_answer_num.replace('A', '')
            else:
                fuz_answer_num = fuz_answer_num.replace('B', '').replace('C', '').replace('D', '')
        elif 'B' in fuz_answer_num:
            pp.xpath('//android.widget.ListView//android.view.View/android.view.View/android.view.View').all()[1] \
                .click()
            time.sleep(3)
            if pp(text="结束本局").exists or pp(text="再来一局").exists:
                fuz_answer_num = fuz_answer_num.replace('B', '')
            else:
                fuz_answer_num = fuz_answer_num.replace('A', '').replace('C', '').replace('D', '')
        elif 'C' in fuz_answer_num:
            pp.xpath('//android.widget.ListView//android.view.View/android.view.View/android.view.View').all()[2] \
                .click()
            time.sleep(3)
            if pp(text="结束本局").exists or pp(text="再来一局").exists:
                fuz_answer_num = fuz_answer_num.replace('C', '')
            else:
                fuz_answer_num = fuz_answer_num.replace('B', '').replace('A', '').replace('D', '')
        elif 'D' in fuz_answer_num:
            pp.xpath('//android.widget.ListView//android.view.View/android.view.View/android.view.View').all()[3] \
                .click()
            time.sleep(3)
            if pp(text="结束本局").exists or pp(text="再来一局").exists:
                fuz_answer_num = fuz_answer_num.replace('D', '')
            else:
                fuz_answer_num = fuz_answer_num.replace('B', '').replace('C', '').replace('A', '')
        else:
            print(f'{fuz_title}在记录中没有正确答案')
        data_ti_ku[fuz_index] = [fuz_title, fuz_choose, fuz_answer_num]
        if new_title_sign == 1:
            with open('ti_ku_verify.json', 'w', encoding='UTF-8') as f2:
                json.dump(data_ti_ku, f2, ensure_ascii=False, indent=2)
        if not (pp(text="结束本局").exists or pp(text="再来一局").exists):
            return True
        else:
            return False


def run_tiao_zhan(ti_num=10):
    pp(text='我要答题').wait()
    pp(text='我要答题').click()
    pp(text='挑战答题').wait()
    pp(text='挑战答题').click()
    with open('ti_ku_verify.json', 'r', encoding="UTF-8") as f1:
        data_ti_ku = json.load(f1)
    duplicate_title_w = []
    for ij, j in enumerate(data_ti_ku):
        for ik, k in enumerate(data_ti_ku):
            if j[0] == k[0] and ij != ik:
                duplicate_title_w.append(j[0])
    duplicate_title_w = list(set(duplicate_title_w))
    dui_num = 0
    while True:
        res = None
        try:
            res = do_tiao_zhan_ti(data_ti_ku, duplicate_title_w)
        except uiautomator2.exceptions.UiObjectNotFoundError:
            pass
        except Exception as e:
            print(e)
        if res:
            dui_num += 1
        else:
            dui_num = 0
        if dui_num == ti_num:
            pp.press('back')
            pp(text='退出').wait()
            pp(text='退出').click()
            break
    time.sleep(3)
    pp.press('back')


def read_issue():
    pp(text='学习积分').wait()
    pp(text='学习积分').click()
    pp(text='积分规则').wait()
    if pp.xpath('//android.widget.ListView/android.view.View[2]/android.view.View[4]').get_text() != '已完成':
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/back_layout"]').wait()  # 从积分界面返回我的界面
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/back_layout"]').click()
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/my_back"]').wait()  # 从我的界面回到APP首页
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/my_back"]').click()
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').wait()  # 点击首页下面的中间学习按钮
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').click()
        pp(text='要闻').wait()
        pp(text='要闻').click()
        for i in range(6):
            t1 = time.time()
            pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i + 1}]').wait()
            pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i + 1}]').click()
            # 阅读文章
            while True:
                pp(scrollable=True).scroll.vert.forward(steps=random.randint(30, 50))
                if time.time() - t1 > 120:
                    break
                time.sleep(1)
                pp(scrollable=True).scroll.vert.backward(steps=random.randint(10, 30))
                time.sleep(1)
            pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]/android.widget.ImageView[1]').wait()  # 收藏
            pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]/android.widget.ImageView[1]').click()  # 收藏
            # 评论，之后删除评论
            pp(text="欢迎发表你的观点").click()  # 评论
            pp(text="好观点将会被优先展示").wait()  # 评论
            pp(text="好观点将会被优先展示").set_text('支持，有希望了，加油，厉害了')  # 评论
            pp(text="发布").wait()  # 评论
            pp(text="发布").click()  # 评论
            pp(text="删除").wait()  # 评论
            while pp(text="删除").exists:
                pp(text="删除").click()  # 评论
                pp.xpath('//*[@resource-id="android:id/button1"]').wait()
                pp.xpath('//*[@resource-id="android:id/button1"]').click()
                time.sleep(2)
            # 分享及返回
            pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]/android.widget.ImageView[2]')\
                .wait()  # 分享
            pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]/android.widget.ImageView[2]')\
                .click()  # 分享
            pp(text="分享到短信").wait()
            pp(text="分享到短信").click()
            pp(text="选择收件人").wait()
            pp(description="向上导航").click()
            pp.press('back')
        time.sleep(2)
        pp(text='我的').wait()
        pp(text='我的').click()
    else:
        print('今日学习文章任务已完成')


def read_video():
    def video_look(ping_dao, nums):
        pp(text=ping_dao).wait()
        for i in range(nums):
            t1 = time.time()
            pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i+1}]').wait()
            pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i+1}]').click()
            # 看视频
            while True:
                pp.screen_on()
                if time.time() - t1 > 180:
                    break
                time.sleep(5)
            pp.press('back')
    pp(text='学习积分').wait()
    pp(text='学习积分').click()
    pp(text='积分规则').wait()
    if pp.xpath('//android.widget.ListView/android.view.View[3]/android.view.View[4]').get_text() != '已完成':
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/back_layout"]').wait()  # 从积分界面返回我的界面
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/back_layout"]').click()
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/my_back"]').wait()  # 从我的界面回到APP首页
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/my_back"]').click()
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').wait()  # 点击首页下面的电视台按钮
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').click()
        video_look('第一频道', 2)
        video_look('联播频道', 4)
        time.sleep(2)
        pp(text='我的').wait()
        pp(text='我的').click()
    else:
        print('今日学习视频任务已完成')


if __name__ == '__main__':
    os.system('adb devices')
    pp = connect()
    pp.unlock()
    # print(pp.dump_hierarchy())
    # raise ()
    if 'cn.xuexi.android' in pp.app_list_running():
        pp.app_stop('cn.xuexi.android')
    pp.app_start('cn.xuexi.android')
    pp(text='我的').wait()
    pp(text='我的').click()
    # run_tiao_zhan()
    # read_issue()
    read_video()
