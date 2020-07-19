import json
import os
import random
import re
import time

import uiautomator2


def connect(serial):
    """
    链接手机     phone = {'lao_po': '3EP7N18C11002513', 'wo_de': '8DF6R16729018868',
     'jiu_de': 'F7R0214305002612', 'ping_ban': '0071ea56'}
    :return: 手机连接引用
    """
    try:
        print('手机的序列号是', serial)
        phone = uiautomator2.connect_usb(serial)
        return phone
    except ConnectionError:
        print('连接手机失败')
        raise ()
    except RuntimeError:
        print('连接手机失败')
        raise ()


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
    time.sleep(1)
    pp(text='我要答题').wait()
    pp(text='我要答题').click()
    pp(text='挑战答题').wait()
    pp(text='挑战答题').click()
    with open('ti_ku_verify.json', 'r', encoding="UTF-8") as f1:
        data_ti_ku = json.load(f1)
    duplicate_title_w = []
    for ij, j1 in enumerate(data_ti_ku):
        for ik, k in enumerate(data_ti_ku):
            if j1[0] == k[0] and ij != ik:
                duplicate_title_w.append(j1[0])
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
            time.sleep(30)
            pp(text='结束本局').wait()
            pp(text='结束本局').click()
            break
    time.sleep(1)
    pp.press('back')
    time.sleep(1)
    pp.press('back')


def read_issue(job_temp):
    try:
        with open(f'data_issue_{learn_num}.json', 'r', encoding="UTF-8") as f1:
            data_issue = json.load(f1)
    except FileNotFoundError:
        data_issue = []
    pp.press('back')  # 从我的界面回到APP首页
    time.sleep(1)
    pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').wait()  # 点击首页下面的中间学习按钮
    pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').click()
    for it, t in enumerate(pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout[1]'
                                    '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]'
                                    '/android.view.ViewGroup[1]//android.widget.LinearLayout'
                                    '/android.widget.TextView').all()):  # 获取文章分类列表
        t.click()
        time.sleep(1)
        for i in range(2, 10):  # 从每个分类中点击前五个文章，例如  要闻
            t2 = time.time()
            con = 0
            while not pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i}]').exists:
                time.sleep(1)
                pp(scrollable=True).scroll(steps=90)
                time.sleep(1)
                if time.time() - t2 > 20:
                    con = 1
                    print(f'定位不到{t.text} 第{i}个文章，跳过')
                    break
            if con == 1:
                continue
            if it in [0, 4, 5, 6]:
                try:
                    title = pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i}]'
                                     f'/android.widget.LinearLayout[1]/android.widget.TextView').get_text()
                except uiautomator2.exceptions.XPathElementNotFoundError:
                    print(f'{t.text} 第{i}个文章标题获取出错，跳过')
                    continue
            if it in [2, 7]:
                try:
                    title = pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i}]'
                                     f'/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]'
                                     f'/android.widget.TextView').get_text()
                except uiautomator2.exceptions.XPathElementNotFoundError:
                    print(f'{t.text} 第{i}个文章标题获取出错，跳过')
                    continue
            elif it in [1, 3]:
                try:
                    title = pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i}]'
                                     f'/android.widget.LinearLayout[1]/android.view.ViewGroup[1]'
                                     f'/android.widget.TextView').get_text()
                except uiautomator2.exceptions.XPathElementNotFoundError:
                    print(f'{t.text} 第{i}个文章标题获取出错，跳过')
                    continue
            else:
                continue
            if title in data_issue:
                print(f'{t.text} {title}  已经看过了，跳过')
                continue
            pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i}]').click()
            print('正在看', t.text, title)
            data_issue.append(title)
            with open(f'data_issue_{learn_num}.json', 'w', encoding='UTF-8') as f2:
                json.dump(data_issue, f2, ensure_ascii=False, indent=2)
            time.sleep(10)  # 每个文章学习七秒
            if job_temp[3] != '已完成':  # 如果没有完成文章学习时长任务，就开始
                t1 = time.time()
                while True:
                    if time.time() - t1 > 110:
                        break
                    pp(scrollable=True).scroll.vert.forward(steps=random.randint(130, 150))
                    time.sleep(1)
                    pp(scrollable=True).scroll.vert.backward(steps=random.randint(110, 130))
                    time.sleep(1)
            if job_temp[10] != '已完成':  # 如果没有完成收藏任务，就开始
                pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                         f'/android.widget.ImageView[1]').wait()  # 收藏
                pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                         f'/android.widget.ImageView[1]').click()  # 收藏
            if job_temp[11] != '已完成':  # 如果没有完成分享任务，就分享及返回
                pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                         f'/android.widget.ImageView[2]').wait()  # 分享
                pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                         f'/android.widget.ImageView[2]').click()  # 分享
                pp(text="分享到短信").wait()
                pp(text="分享到短信").click()
                time.sleep(1)
                while not pp.xpath(
                        f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                        f'/android.widget.ImageView[1]').exists:
                    pp.press('back')
                    time.sleep(1)
                time.sleep(1)
            if job_temp[12] != '已完成':  # 如果没有完成评论任务，就开始评论，之后删除评论
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
                    time.sleep(1)
            pp.press('back')  # 学习完每一篇文章后返回
            time.sleep(1)
            pp(text='我的').wait()
            pp.xpath('//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click()  # 点击积分,查一下积分完成情况
            job_temp = job_status()  # 查一下积分完成情况
            if job_temp[1] == '已完成':  # 如果学习文章没完成，就开始学习//android.widget.ListView/android.widget.FrameLayout[4]
                pp(text='我的').wait()
                pp(text='我的').click()
                print('阅读文章任务已完成')
                return


def read_video(job_temp):
    try:
        with open(f'data_video_{learn_num}.json', 'r', encoding="UTF-8") as f1:
            data_video = json.load(f1)
    except FileNotFoundError:
        data_video = []
    time.sleep(1)
    pp.press('back')  # 从我的界面回到APP首页
    time.sleep(1)
    pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').wait()  # 点击首页下面的电视台按钮
    pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').click()
    for it, t in enumerate(pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout[1]'
                                    '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/'
                                    'android.view.ViewGroup[1]//android.widget.LinearLayout').all()):  # 获取视频分类列表
        t.click()
        time.sleep(1)
        for i in range(2, 10):
            t2 = time.time()
            con = 0
            while not pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i}]').exists:
                time.sleep(1)
                pp(scrollable=True).scroll(steps=90)
                time.sleep(1)
                if time.time() - t2 > 20:
                    con = 1
                    print(f'定位不到{t.text} 第{i}个视频，跳过')
                    break
            if con == 1:
                continue
            if it in [2]:
                try:
                    title = pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i}]'
                                     f'/android.widget.LinearLayout[1]/android.widget.TextView').get_text()
                except uiautomator2.exceptions.XPathElementNotFoundError:
                    print(f'{t.text} 第{i}个视频标题获取出错，跳过')
                    continue
            elif it in [1, 4, 5]:
                try:
                    title = pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i}]'
                                     f'/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]'
                                     f'/android.widget.TextView').get_text()
                except uiautomator2.exceptions.XPathElementNotFoundError:
                    print(f'{t.text} 第{i}个视频标题获取出错，跳过')
                    continue
            elif it in [0]:
                try:
                    title = pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i}]'
                                     f'/android.widget.LinearLayout[1]/android.view.ViewGroup[1]'
                                     f'/android.widget.TextView').get_text()
                except uiautomator2.exceptions.XPathElementNotFoundError:
                    print(f'{t.text} 第{i}个视频标题获取出错，跳过')
                    continue
            else:
                continue
            if title in data_video:
                print(f'{t.text} {title}  已经看过了，跳过')
                continue
            data_video.append(title)
            with open(f'data_video_{learn_num}.json', 'w', encoding='UTF-8') as f2:
                json.dump(data_video, f2, ensure_ascii=False, indent=2)
            pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i}]').click()
            time.sleep(1)  # 每个视频学习10秒
            if pp(text='继续播放').exists:
                pp(text='继续播放').click()
            time.sleep(10)  # 每个视频学习10秒
            if job_temp[4] != '已完成':  # 如果没有完成视频学习时长任务，就开始
                t1 = time.time()
                while True:
                    if time.time() - t1 > 180:
                        break
                    pp(text='点赞').click()
                    time.sleep(1)
            pp.press('back')  # 学习完每一个视频后返回
            time.sleep(1)
            pp(text='我的').wait()
            pp.xpath('//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click()  # 点击积分,查一下积分完成情况
            job_temp = job_status()  # 查一下积分完成情况
            time.sleep(1)
            if job_temp[2] == '已完成':  # 如果学习视频没完成，就开始学习//android.widget.ListView/android.widget.FrameLayout[4]
                time.sleep(1)
                pp(text='我的').wait()
                pp(text='我的').click()
                print('看视频任务已完成')
                return


def look_tel(job_temp):  # 看电视台的视频
    time.sleep(1)
    pp.press('back')  # 从我的界面回到APP首页
    time.sleep(1)
    pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').wait()  # 点击首页下面的电视台按钮
    pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').click()
    time.sleep(1)
    pp(text='看电视').wait()
    pp(text='看电视').click()
    time.sleep(1)
    for i in range(1, 7):
        t2 = time.time()
        con = 0
        while not pp.xpath(f'//android.support.v7.widget.RecyclerView/android.widget.FrameLayout[{i}]').exists:
            time.sleep(1)
            pp(scrollable=True).scroll(steps=90)
            time.sleep(1)
            if time.time() - t2 > 20:
                con = 1
                print(f'定位不到第{i}个视频，跳过')
                break
        if con == 1:
            continue
        pp.xpath(f'//android.support.v7.widget.RecyclerView/android.widget.FrameLayout[{i}]').click()
        time.sleep(1)  # 每个视频学习10秒
        if pp(text='继续播放').exists:
            pp(text='继续播放').click()
        time.sleep(10)  # 每个视频学习10秒
        if job_temp[4] != '已完成':  # 如果没有完成视频学习时长任务，就开始
            t1 = time.time()
            while True:
                if time.time() - t1 > 180:
                    break
                pp.screen_on()
                time.sleep(1)
        pp(text='我的').wait()
        pp.xpath('//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click()  # 点击积分,查一下积分完成情况
        job_temp = job_status()  # 查一下积分完成情况
        time.sleep(1)
        if job_temp[2] == '已完成':  # 如果学习视频没完成，就开始学习//android.widget.ListView/android.widget.FrameLayout[4]
            time.sleep(1)
            pp(text='我的').wait()
            pp(text='我的').click()
            print('看视频任务已完成')
            return


def ding_yue():
    time.sleep(1)
    pp(text='订阅').wait()
    pp(text='订阅').click()
    time.sleep(1)
    pp(text='添加').wait()
    pp(text='添加').click()
    for i in range(8):
        if pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i + 1}]/android.widget.LinearLayout[2]') \
                .exists:
            pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i + 1}]/android.widget.LinearLayout[2]') \
                .click()
            time.sleep(1)
            pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout[{i + 1}]/android.widget.LinearLayout[2]') \
                .click()
        time.sleep(1)
    print('已完成订阅')
    pp.press("back")
    pp(text='我的订阅').wait()
    pp.press("back")


def ben_di():
    time.sleep(1)
    pp.press("back")
    time.sleep(1)
    pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout['
             '1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.view.ViewGroup['
             '1]/android.widget.LinearLayout[4]').wait()
    pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout['
             '1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.view.ViewGroup['
             '1]/android.widget.LinearLayout[4]').click()
    time.sleep(1)
    pp.xpath('//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]').wait()
    pp.xpath('//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]').click()
    print('已完成本地频道')
    time.sleep(1)
    pp.press('back')
    pp(text='我的').wait()
    pp(text='我的').click()


def job_status():
    time.sleep(1)
    job_status1 = []
    for j in range(1, 15):
        while not pp.xpath(f'//android.widget.ListView/android.view.View[{j}]/android.view.View[4]').exists:
            pp(scrollable=True).scroll(steps=100)
            time.sleep(1)
        job_status1.append(pp.xpath(f'//android.widget.ListView/'
                                    f'android.view.View[{j}]/android.view.View[4]').get_text())
    pp.press('back')  # 查一下积分完成情况
    time.sleep(1)
    return job_status1


if __name__ == '__main__':
    fp = os.popen('adb devices').readlines()
    if 'List of devices attached' in fp[0] and 'device' in fp[1]:
        phone_serial = re.search(r'(.*)\t', fp[1]).group().strip()
    else:
        phone_serial = None
    pp = connect(phone_serial)
    pp.unlock()
    # pp(scrollable=True).scroll(steps=90)
    # print(pp.dump_hierarchy())
    # raise ()
    if 'cn.xuexi.android' in pp.app_list_running():
        pp.app_stop('cn.xuexi.android')
    pp.app_start('cn.xuexi.android')
    pp(text='我的').wait()
    pp(text='我的').click()
    time.sleep(1)
    pp(description='我的信息').wait()
    pp(description='我的信息').click()
    time.sleep(1)
    learn_num = pp.xpath('//*[@resource-id="cn.xuexi.android:id/user_info_fragment_container"]'
                         '/android.widget.LinearLayout[3]/android.widget.LinearLayout[1]'
                         '/android.widget.TextView[2]').get_text()
    print('这个手机学习强国的学号是', learn_num)
    pp.press('back')
    time.sleep(1)
    pp(text='学习积分').wait()
    pp(text='学习积分').click()
    pp(text='积分规则').wait()
    job_stat = job_status()
    pp(text='我的').wait()
    # read_issue(job_stat)
    # raise ()
    if job_stat[1] != '已完成':
        read_issue(job_stat)
    else:
        print('已完成文章阅读')
    if job_stat[2] != '已完成':
        # look_tel(job_stat)
        read_video(job_stat)
    else:
        print('已完成视频观看')
    if job_stat[8] != '已完成':
        run_tiao_zhan()
    else:
        print('已完成挑战答题')
    if job_stat[9] != '已完成':
        ding_yue()
    else:
        print('已完成订阅')
    if job_stat[13] != '已完成':
        ben_di()
    else:
        print('已完成本地频道')
    pp(text='学习积分').click()
