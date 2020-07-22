import json
import os
import random
import re
import time
import pytesseract
import uiautomator2
from fuzzywuzzy import fuzz, process


class FuckQiangGuo(object):
    def __init__(self):
        super(FuckQiangGuo, self).__init__()
        self.pp = self.connect_phone_usb()
        # self.pp = uiautomator2.connect('127.0.0.1:62001')
        self.duplicate_title = []
        self.learn_num = None

    @staticmethod
    def connect_phone_usb():
        """
        链接手机     phone = {'lao_po': '3EP7N18C11002513', 'wo_de': '8DF6R16729018868',
         'jiu_de': 'F7R0214305002612', 'ping_ban': '0071ea56'}
        :return: 手机连接引用
        """
        fp = os.popen('adb devices').readlines()
        if 'List of devices attached' in fp[0] and 'device' in fp[1]:
            phone_serial = re.search(r'(.*)\t', fp[1]).group().strip()
        else:
            phone_serial = None
        try:
            print('手机的序列号是', phone_serial)
            phone = uiautomator2.connect_usb(phone_serial)
            return phone
        except ConnectionError:
            print('连接手机失败')
            raise ()
        except RuntimeError:
            print('连接手机失败')
            raise ()

    def do_tiao_zhan_ti(self, data_ti_ku):  # 挑战答题主程序，用来做一个题
        if self.pp(text="结束本局").exists:
            self.pp(text="结束本局").click()
            time.sleep(1)
            self.pp(text='再来一局').wait()
            time.sleep(1)
            self.pp(text='再来一局').click()
        if self.pp(text="再来一局").exists:
            self.pp(text='再来一局').click()
        if self.pp(text="选择联系人").exists:
            self.pp(description="返回").click()
        self.pp.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View['
                      '1]/android.view.View[1]/android.view.View[1]').wait()
        title = self.pp.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/'
                              'android.view.View[1]/android.view.View[2]/android.view.View[1]/'
                              'android.view.View[1]').get_text()  # 匹配标题
        title = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(title).replace('\xa0', '').replace('_', ''))  # 清洗，除去字符等
        answer = [ans.text for ans in
                  self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/android'
                                '.view.View').all()]
        fuz_title = None
        fuz_choose = None
        fuz_answer_num = None
        fuz_index = None
        for index, num in enumerate(data_ti_ku):
            if title in self.duplicate_title and title == num[0] and answer == num[1]:
                fuz_index = index
                fuz_title = num[0]
                fuz_choose = num[1]
                fuz_answer_num = num[2]
                break
            elif title not in self.duplicate_title and title == num[0]:
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
            self.duplicate_title = list(set(self.duplicate_title.append(fuz_title)))
            with open('ti_ku_verify.json', 'w', encoding='UTF-8') as f2:
                json.dump(data_ti_ku, f2, ensure_ascii=False, indent=2)
        else:  # 匹配到了
            # print('匹配到了', fuz_title, answer, '匹配的答案是', fuz_answer_num)
            if len(fuz_answer_num) > 1:
                new_title_sign = 1
                self.duplicate_title = list(set(self.duplicate_title.append(fuz_title)))
                print('新加入的题匹配到了', fuz_title, answer, '匹配的答案是', fuz_answer_num)
            if 'A' in fuz_answer_num:
                self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/android.view.View').all()[
                    0] \
                    .click()
                if fuz_answer_num == 'ABCD':
                    img_a = self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                                          'android.view.View').all()[0].screenshot()
                    r, g, b = img_a.resize((1, 1)).getpixel((0, 0))
                    if 230 > g > 150 > b > 100 > r > 50:
                        fuz_answer_num = 'A'
                        print(title, answer, 'A')
                time.sleep(1)
                # if self.pp(text="结束本局").exists or self.pp(text="再来一局").exists:
                #     fuz_answer_num = fuz_answer_num.replace('A', '')
                # else:
                #     fuz_answer_num = fuz_answer_num.replace('B', '').replace('C', '').replace('D', '')
            elif 'B' in fuz_answer_num:
                self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/android.view.View').all()[
                    1] \
                    .click()
                if fuz_answer_num == 'ABCD':
                    img_b = self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                                          'android.view.View').all()[0].screenshot()
                    r, g, b = img_b.resize((1, 1)).getpixel((0, 0))
                    if 230 > g > 150 > b > 100 > r > 50:
                        fuz_answer_num = 'B'
                        print(title, answer, 'B')
                time.sleep(1)
                # if self.pp(text="结束本局").exists or self.pp(text="再来一局").exists:
                #     fuz_answer_num = fuz_answer_num.replace('B', '')
                # else:
                #     fuz_answer_num = fuz_answer_num.replace('A', '').replace('C', '').replace('D', '')
            elif 'C' in fuz_answer_num:
                self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/android.view.View').all()[
                    2] \
                    .click()
                if fuz_answer_num == 'ABCD':
                    img_c = self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                                          'android.view.View').all()[0].screenshot()
                    r, g, b = img_c.resize((1, 1)).getpixel((0, 0))
                    if 230 > g > 150 > b > 100 > r > 50:
                        fuz_answer_num = 'C'
                        print(title, answer, 'C')
                time.sleep(1)
                # if self.pp(text="结束本局").exists or self.pp(text="再来一局").exists:
                #     fuz_answer_num = fuz_answer_num.replace('C', '')
                # else:
                #     fuz_answer_num = fuz_answer_num.replace('B', '').replace('A', '').replace('D', '')
            elif 'D' in fuz_answer_num:
                self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/android.view.View').all()[
                    3] \
                    .click()
                if fuz_answer_num == 'ABCD':
                    img_d = self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                                          'android.view.View').all()[0].screenshot()
                    r, g, b = img_d.resize((1, 1)).getpixel((0, 0))
                    if 230 > g > 150 > b > 100 > r > 50:
                        fuz_answer_num = 'D'
                        print(title, answer, 'D')
                time.sleep(1)
                # if self.pp(text="结束本局").exists or self.pp(text="再来一局").exists:
                #     fuz_answer_num = fuz_answer_num.replace('D', '')
                # else:
                #     fuz_answer_num = fuz_answer_num.replace('B', '').replace('C', '').replace('A', '')
            else:
                print(f'{fuz_title}在记录中没有正确答案,')
                fuz_answer_num = 'ABCD'
            data_ti_ku[fuz_index] = [fuz_title, fuz_choose, fuz_answer_num]
            if new_title_sign == 1:
                with open('ti_ku_verify.json', 'w', encoding='UTF-8') as f2:
                    json.dump(data_ti_ku, f2, ensure_ascii=False, indent=2)
            if not (self.pp(text="结束本局").exists or self.pp(text="再来一局").exists):
                return True
            else:
                return False

    def run_tiao_zhan(self, ti_num=10):
        time.sleep(1)
        self.pp(text='我要答题').wait()
        self.pp(text='我要答题').click()
        self.pp(text='挑战答题').wait()
        self.pp(text='挑战答题').click()
        with open('ti_ku_verify.json', 'r', encoding="UTF-8") as f1:
            data_ti_ku = json.load(f1)
        for ij, j1 in enumerate(data_ti_ku):
            for ik, k in enumerate(data_ti_ku):
                if j1[0] == k[0] and ij != ik:
                    self.duplicate_title.append(j1[0])
        self.duplicate_title = list(set(self.duplicate_title))
        dui_num = 0
        while True:
            res = None
            try:
                res = self.do_tiao_zhan_ti(data_ti_ku)
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
                self.pp(text='结束本局').wait()
                self.pp(text='结束本局').click()
                break
        time.sleep(1)
        self.pp.press('back')
        time.sleep(1)
        self.pp.press('back')

    @staticmethod
    def pic_to_text(ti_shi_pic):
        width, height = ti_shi_pic.size
        split_height = []
        pic_text_num = 0
        for h in range(height):  # 获取白色分割线的高度信息，为计算分几块识别图片作准备
            for w in range(width):
                color = ti_shi_pic.getpixel((w, h))
                if color[0] > 250 and color[1] > 250 and color[2] > 250:
                    if w == width - 1:
                        split_height.append(h)
                else:
                    break
        # print(split_height)
        for i, k in enumerate(split_height):  # 计算将提示的图片分几个区域
            try:
                if k <= split_height[i - 1] + 10:
                    pass
                else:
                    pic_text_num += 1
            except IndexError:
                pass
        # raise
        ti_shi_word = ''
        for p in range(pic_text_num):  # 识别，把不是红色的地方都变白色。
            img = ti_shi_pic.crop((0, int(height / pic_text_num * p), width, int(height / pic_text_num * (p + 1))))
            for w in range(width):
                for h in range(int(height / pic_text_num)):
                    color = img.getpixel((w, h))
                    if color[0] > 150 and color[1] < 140 and color[2] < 140:
                        pass
                    else:
                        img.putpixel((w, h), (255, 255, 255))
            # img.show()
            pic_str = pytesseract.image_to_string(img, lang='chi_sim')
            pic_str = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(pic_str).replace('\xa0', '').replace('_', ''))
            # if not pic_str:
            #     img.save(f'{split_height} {kuai_num}.png')
            # print(pic_str)
            ti_shi_word += pic_str
        return ti_shi_word

    @staticmethod
    def video_to_text():
        return 'wwo le qu ge ren a ha ah'

    def do_everyday_ti(self):
        self.pp.xpath('//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]'
                      '/android.view.View[1]/android.view.View[1]/android.view.View').wait()
        ti_type = self.pp.xpath('//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]'
                                '/android.view.View[1]/android.view.View[1]/android.view.View').get_text()
        video = self.pp.xpath('//android.widget.Image').exists
        # print(ti_type)
        self.pp(scrollable=True).scroll.toEnd()
        self.pp(text='查看提示').wait()
        self.pp(text='查看提示').click()
        time.sleep(1)
        # ti_shi = self.pp.xpath('//*[@resource-id="app"]/android.view.View[2]/android.view.View[3]'
        #                   '/android.view.View[2]/android.view.View').get_text()
        # ti_shi = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(ti_shi).replace('\xa0', '').replace('_', ''))
        ti_shi_pic = self.pp.xpath('//*[@resource-id="app"]/android.view.View[2]/android.view.View[3]'
                                   '/android.view.View[2]/android.view.View').screenshot()
        if video:
            ti_shi_word = self.video_to_text()
        else:
            ti_shi_word = self.pic_to_text(ti_shi_pic)
        # print('提示中获取到的关键词是 ', ti_shi_word)
        # raise
        self.pp.press('back')
        time.sleep(1)
        self.pp(scrollable=True).scroll.toBeginning()
        if ti_type == '填空题':
            if self.pp(className='android.widget.EditText').count == 1:
                self.pp(className='android.widget.EditText').set_text(ti_shi_word)
            else:
                for self.pp1 in self.pp(className='android.widget.EditText'):
                    text_len = self.pp1.sibling(className="android.view.View").count
                    ti_shi_word_temp = ti_shi_word[:text_len]
                    self.pp1.set_text(ti_shi_word_temp)
                    ti_shi_word = ti_shi_word.replace(ti_shi_word_temp, '')
                    # print(ti_shi_word, ti_shi_word_temp)
            time.sleep(1)
            if self.pp(text='确定').exists:
                self.pp(text='确定').click()
                time.sleep(1)
                if self.pp(text='下一题').exists:
                    self.pp(text='下一题').click()
                elif self.pp(text='完成').exists:
                    self.pp(text='完成').click()
            else:
                # print('没找到完全匹配的答案，随便填写了')
                for self.pp2 in self.pp(className='android.widget.EditText'):
                    self.pp2.set_text('wolegequashoubuliaole')
                time.sleep(1)
                if not self.pp(text='确定').exists:
                    print('这个填空题没法自动答题，手动答题吧')
                    raise
                else:
                    self.pp(text='确定').wait()
                    self.pp(text='确定').click()
                    time.sleep(1)
                    if self.pp(text='下一题').exists:
                        self.pp(text='下一题').click()
                    elif self.pp(text='完成').exists:
                        self.pp(text='完成').click()
        else:
            answer = []
            for choose in self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View[1]'
                                        '/android.view.View[2]').all():
                answer.append(choose.text)
                if choose.text in ti_shi_word or fuzz.partial_ratio(choose.text, ti_shi_word) > 90:
                    choose.click()
            time.sleep(1)
            if self.pp(text='确定').exists:
                self.pp(text='确定').click()
                time.sleep(1)
                if self.pp(text='下一题').exists:
                    self.pp(text='下一题').click()
                elif self.pp(text='完成').exists:
                    self.pp(text='完成').click()
            else:
                # print('没找到完全匹配的答案，找个最合适的')
                da_an = str(process.extractOne(ti_shi_word, answer)[0])
                self.pp(text=da_an).click()
                time.sleep(1)
                if not self.pp(text='确定').exists:
                    print('这个选择题没法自动答题，手动答题吧')
                    raise
                else:
                    self.pp(text='确定').wait()
                    self.pp(text='确定').click()
                    time.sleep(1)
                    if self.pp(text='下一题').exists:
                        self.pp(text='下一题').click()
                    elif self.pp(text='完成').exists:
                        self.pp(text='完成').click()

    def run_everyday_ti(self):
        time.sleep(1)
        self.pp(text='我要答题').wait()
        self.pp(text='我要答题').click()
        self.pp(text='每日答题').wait()
        self.pp(text='每日答题').click()
        time.sleep(1)
        while True:
            self.do_everyday_ti()
            time.sleep(1)
            if self.pp(text='再来一组').exists:
                self.pp(text='返回').click()
                time.sleep(1)
                self.pp.press('back')
                time.sleep(1)
                self.pp(text='学习积分').wait()
                self.pp(text='学习积分').click()
                time.sleep(1)
                job_sta = self.job_status()
                if job_sta[5] == '已完成':
                    break
                time.sleep(1)
                self.pp(text='我要答题').wait()
                self.pp(text='我要答题').click()
                self.pp(text='每日答题').wait()
                self.pp(text='每日答题').click()
                time.sleep(1)

    def read_issue(self, job_temp, test=False):
        try:
            with open(f'data_issue_{self.learn_num}.json', 'r', encoding="UTF-8") as f1:
                data_issue = json.load(f1)
        except FileNotFoundError:
            data_issue = []
        self.pp.press('back')  # 从我的界面回到app首页
        time.sleep(1)
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').wait()  # 点击首页下面的中间学习按钮
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').click()
        for it, t in enumerate(
                self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout[1]'
                              '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]'
                              '/android.view.ViewGroup[1]//android.widget.LinearLayout'
                              '/android.widget.TextView').all()):  # 获取文章分类列表
            t.click()
            time.sleep(1)
            for ci_shu in range(8):
                for isu, issue in enumerate(
                        self.pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout').all()):
                    loc = issue.center()
                    self.pp.click(*loc)
                    time.sleep(1)
                    if self.pp(text='我的').exists:
                        continue
                    try:
                        title = self.pp.xpath(f'//*[@resource-id="xxqg-article-header"]/android.view.View[1]') \
                            .get(timeout=1).text
                    except uiautomator2.exceptions.XPathElementNotFoundError:
                        if not self.pp(text='我的').exists:
                            self.pp.press('back')
                        print(f'{t.text} 第{isu}个文章标题获取出错，跳过')
                        continue
                    if title in data_issue:
                        self.pp.press('back')
                        print(f'{t.text} {title}  已经看过了，跳过')
                        continue
                    print('正在看', t.text, title)
                    data_issue.append(title)
                    with open(f'data_issue_{self.learn_num}.json', 'w', encoding='UTF-8') as f2:
                        json.dump(data_issue, f2, ensure_ascii=False, indent=2)
                    time.sleep(10)  # 每个文章学习七秒
                    if job_temp[3] != '已完成':  # 如果没有完成文章学习时长任务，就开始
                        t1 = time.time()
                        while True:
                            if time.time() - t1 > 110:
                                break
                            self.pp(scrollable=True).scroll.vert.forward(steps=random.randint(130, 150))
                            time.sleep(1)
                            self.pp(scrollable=True).scroll.vert.backward(steps=random.randint(110, 130))
                            time.sleep(1)
                    if job_temp[10] != '已完成':  # 如果没有完成收藏任务，就开始
                        self.pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                                      f'/android.widget.ImageView[1]').wait()  # 收藏
                        self.pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                                      f'/android.widget.ImageView[1]').click()  # 收藏
                        time.sleep(1)
                        if self.pp(text='我知道了').exists:
                            self.pp(text='我知道了').click()
                            time.sleep(1)
                    if job_temp[11] != '已完成':  # 如果没有完成分享任务，就分享及返回
                        self.pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                                      f'/android.widget.ImageView[2]').wait()  # 分享
                        self.pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                                      f'/android.widget.ImageView[2]').click()  # 分享
                        self.pp(text="分享到短信").wait()
                        self.pp(text="分享到短信").click()
                        time.sleep(1)
                        while not self.pp.xpath(
                                f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                                f'/android.widget.ImageView[1]').exists:
                            self.pp.press('back')
                            time.sleep(1)
                        time.sleep(1)
                    if job_temp[12] != '已完成':  # 如果没有完成评论任务，就开始评论，之后删除评论
                        self.pp(text="欢迎发表你的观点").click()  # 评论
                        self.pp(text="好观点将会被优先展示").wait()  # 评论
                        self.pp(text="好观点将会被优先展示").set_text('支持，有希望了，加油，厉害了')  # 评论
                        self.pp(text="发布").wait()  # 评论
                        self.pp(text="发布").click()  # 评论
                        self.pp(text="删除").wait()  # 评论
                        while self.pp(text="删除").exists:
                            self.pp(text="删除").click()  # 评论
                            self.pp.xpath('//*[@resource-id="android:id/button1"]').wait()
                            self.pp.xpath('//*[@resource-id="android:id/button1"]').click()
                            time.sleep(1)
                    self.pp.press('back')  # 学习完每一篇文章后返回
                    time.sleep(1)
                    if not test:
                        self.pp(text='我的').must_wait()
                        self.pp.xpath(
                            '//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click()  # 点击积分,查一下积分完成情况
                        job_temp = self.job_status()  # 查一下积分完成情况
                        if job_temp[1] == '已完成':  # 如果学习文章没完成，就开始学习
                            self.pp(text='我的').wait()
                            self.pp(text='我的').click()
                            print('阅读文章任务已完成')
                            return
                time.sleep(1)
                if it == 0:
                    self.pp(scrollable=True).scroll.toEnd(steps=90, max_swipes=4)
                else:
                    self.pp(scrollable=True).scroll(steps=90)
                time.sleep(1)

    def read_video(self, test=False):
        try:
            with open(f'data_video_{self.learn_num}.json', 'r', encoding="UTF-8") as f1:
                data_video = json.load(f1)
        except FileNotFoundError:
            data_video = []
        time.sleep(1)
        self.pp.press('back')  # 从我的界面回到app首页
        time.sleep(1)
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').wait()  # 点击首页下面的电视台按钮
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').click()
        for it, t in enumerate(
                self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout[1]'
                              '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/'
                              'android.view.ViewGroup[1]//android.widget.LinearLayout/'
                              'android.widget.TextView').all()):  # 获取视频分类列表
            t.click()
            time.sleep(1)
            for ci_shu in range(8):
                for isu, issue in enumerate(
                        self.pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout').all()):
                    loc = issue.center()
                    self.pp.click(*loc)
                    time.sleep(1)
                    if self.pp(text='我的').exists:
                        continue
                    try:
                        title = self.pp.xpath(f'//*[@resource-id="xxqg-article-body"]/android.view.View[2]') \
                            .get(timeout=1).text
                    except uiautomator2.exceptions.XPathElementNotFoundError:
                        if not self.pp(text='我的').exists:
                            self.pp.press('back')
                        print(f'{t.text} 第{isu}个视频标题获取出错，跳过')
                        continue
                    if title in data_video:
                        self.pp.press('back')
                        print(f'{t.text} {title}  已经看过了，跳过')
                        continue
                    print('正在看', t.text, title)
                    data_video.append(title)
                    with open(f'data_video_{self.learn_num}.json', 'w', encoding='UTF-8') as f2:
                        json.dump(data_video, f2, ensure_ascii=False, indent=2)
                    time.sleep(1)  # 每个视频学习10秒
                    if self.pp(text='继续播放').exists:
                        self.pp(text='继续播放').click()
                    time.sleep(9)  # 每个视频学习10秒
                    # if job_temp[4] != '已完成':  # 如果没有完成视频学习时长任务，就开始，改成学习视频时长用看电视的方法，
                    #     t1 = time.time()
                    #     while True:
                    #         if time.time() - t1 > 180:
                    #             break
                    #         self.pp(text='点赞').click()
                    #         time.sleep(1)
                    self.pp.press('back')  # 学习完每一个视频后返回
                    time.sleep(1)
                    if not test:
                        self.pp(text='我的').wait()
                        self.pp.xpath(
                            '//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click()  # 点击积分,查一下积分完成情况
                        job_temp = self.job_status()  # 查一下积分完成情况
                        time.sleep(1)
                        if job_temp[2] == '已完成':  # 如果学习视频没完成，就开始学习
                            time.sleep(1)
                            self.pp(text='我的').wait()
                            self.pp(text='我的').click()
                            print('看视频任务已完成')
                            return
                time.sleep(1)
                self.pp(scrollable=True).scroll(steps=90)
                time.sleep(1)

    def look_tel(self):  # 看电视台的视频，主要是用来弥补视频学习时长
        time.sleep(1)
        self.pp.press('back')  # 从我的界面回到app首页
        time.sleep(1)
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').wait()  # 点击首页下面的电视台按钮
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').click()
        time.sleep(1)
        self.pp(text='看电视').wait()
        self.pp(text='看电视').click()
        time.sleep(1)
        while True:
            if not self.pp.xpath(f'//android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]').exists:
                self.pp(scrollable=True).scroll(steps=90)
                time.sleep(1)
            try:
                self.pp.xpath(f'//android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]').click()
            except uiautomator2.exceptions.XPathElementNotFoundError:
                print('找不到CCTV-2电视台，不能播放，不看电视了')
                return
            time.sleep(1)  # 每个视频学习
            if self.pp(text='继续播放').exists:
                self.pp(text='继续播放').click()
            t1 = time.time()
            while True:
                if time.time() - t1 > 180:
                    break
                self.pp.screen_on()
                time.sleep(1)
            self.pp(text='我的').wait()
            self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click()  # 点击积分,查一下积分完成情况
            job_temp = self.job_status()  # 查一下积分完成情况
            time.sleep(1)
            if job_temp[4] == '已完成':  # 如果视频学习时长任务没完成，就开始学习
                self.pp(text='我的').wait()
                self.pp(text='我的').click()
                print('看视频任务已完成')
                return

    def ding_yue(self):
        time.sleep(1)
        self.pp(text='订阅').wait()
        self.pp(text='订阅').click()
        time.sleep(1)
        self.pp(text='添加').wait()
        self.pp(text='添加').click()
        time.sleep(1)
        for i in self.pp.xpath(f'//android.widget.ListView//android.widget.FrameLayout'
                               f'/android.widget.LinearLayout[2]/android.widget.ImageView[1]').all():
            if i.attrib['content-desc'] == '订阅':
                i.click()
                time.sleep(1)
                i.click()
            else:
                i.click()
                time.sleep(1)
                i.click()
                time.sleep(1)
                i.click()
            time.sleep(1)
        print('已完成订阅')
        self.pp.press("back")
        self.pp(text='我的订阅').wait()
        self.pp.press("back")

    def ben_di(self):
        time.sleep(1)
        self.pp.press("back")
        time.sleep(1)
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout['
                      '1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.view.ViewGroup['
                      '1]/android.widget.LinearLayout[4]').wait()
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout['
                      '1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.view.ViewGroup['
                      '1]/android.widget.LinearLayout[4]').click()
        time.sleep(1)
        self.pp.xpath('//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]').wait()
        self.pp.xpath('//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]').click()
        print('已完成本地频道')
        time.sleep(1)
        self.pp.press('back')
        self.pp(text='我的').wait()
        self.pp(text='我的').click()

    def job_status(self):
        time.sleep(1)
        job_status1 = []
        for j in range(1, 15):
            while not self.pp.xpath(f'//android.widget.ListView/android.view.View[{j}]/android.view.View[4]').exists:
                self.pp(scrollable=True).scroll(steps=100)
                time.sleep(1)
            job_status1.append(self.pp.xpath(f'//android.widget.ListView/'
                                             f'android.view.View[{j}]/android.view.View[4]').get_text())
        self.pp.press('back')  # 查一下积分完成情况
        time.sleep(1)
        return job_status1

    def main_do(self):  # 主运行程序
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        self.pp.unlock()
        # print(self.pp.dump_hierarchy())
        # run_everyday_ti()
        # self.run_tiao_zhan(ti_num=9999)
        # raise ()
        if 'cn.xuexi.android' in self.pp.app_list_running():
            self.pp.app_stop('cn.xuexi.android')
        self.pp.app_start('cn.xuexi.android')
        self.pp(text='我的').wait()
        self.pp(text='我的').click()
        time.sleep(1)
        self.pp(description='我的信息').wait()
        self.pp(description='我的信息').click()
        time.sleep(1)
        self.learn_num = self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/user_info_fragment_container"]'
                                       '/android.widget.LinearLayout[3]/android.widget.LinearLayout[1]'
                                       '/android.widget.TextView[2]').get_text()
        print('这个手机学习强国的学号是', self.learn_num)
        self.pp.press('back')
        time.sleep(1)
        self.pp(text='学习积分').wait()
        self.pp(text='学习积分').click()
        self.pp(text='积分规则').wait()
        job_stat = self.job_status()
        self.pp(text='我的').wait()
        print(job_stat)
        # look_tel()
        # raise ()
        if job_stat[1] != '已完成':
            self.read_issue(job_stat)
        else:
            print('已完成文章阅读')
        if job_stat[2] != '已完成':
            self.read_video()
        else:
            print('已完成视频观看')
        if job_stat[4] != '已完成':
            self.look_tel()
        else:
            print('已完成视听时长学习')
        if job_stat[5] != '已完成':
            self.run_everyday_ti()
        else:
            print('已完成每日答题任务')
        if job_stat[8] != '已完成':
            self.run_tiao_zhan()
        else:
            print('已完成挑战答题')
        if job_stat[9] != '已完成':
            self.ding_yue()
        else:
            print('已完成订阅')
        if job_stat[13] != '已完成':
            self.ben_di()
        else:
            print('已完成本地频道')
        self.pp(text='学习积分').click()


if __name__ == '__main__':
    do = FuckQiangGuo()
    do.main_do()
