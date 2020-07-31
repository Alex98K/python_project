import json
import os
import random
import re
import time
import pytesseract
import uiautomator2
from fuzzywuzzy import process


class QiangGuoFuZhu(object):
    def __init__(self, tesseract_path=r'C:/Program Files/Tesseract-OCR/tesseract.exe'):
        super(QiangGuoFuZhu, self).__init__()
        self.path = os.path.abspath(os.path.dirname(__file__))
        pytesseract.pytesseract.tesseract_cmd = tesseract_path  # tesseract可执行文件的路径
        self.pp = self.connect_phone_usb()
        # self.pp = uiautomator2.connect_wifi('192.168.1.218')
        # self.pp = uiautomator2.connect('127.0.0.1:62001')
        self.duplicate_title = []
        self.learn_num = None
        # 注册watcher，如果顶部的快捷栏被无意间滑下来了，就自动返回，划上去
        self.pp.watcher('notification').when(xpath="//*[@resource-id='com.android.systemui:id"
                                                   "/notification_container_parent']").call(self.call_back)
        self.pp.watcher.start(0.2)

    def __del__(self):
        try:
            self.pp.watcher.stop()
        except AttributeError:
            pass

    def call_back(self):
        self.pp(resourceId="com.android.systemui:id/notification_container_parent").scroll.vert.forward(steps=10)

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
            print('连接手机失败, 请拔了USB线，重新插入')
            raise ()
        except RuntimeError:
            print('连接手机失败, 请拔了USB线，重新插入')
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
        answer = [ans.text for ans in self.pp.xpath('//android.widget.ListView//android.view.View/'
                                                    'android.view.View/android.view.View').all()]  # 获取答案选项列表
        fuz_title = None  # 匹配的标题
        fuz_choose = None  # 匹配的答案选项
        fuz_answer_num = None  # 匹配的题库中的选项
        fuz_index = None  # 匹配的题目在题库列表中的索引
        for index, num in enumerate(data_ti_ku):  # 匹配题库
            if title in self.duplicate_title and title == num[0] and answer == num[1]:  # 标题在重复列表中的，标题和选项全一样的才能算匹配到
                fuz_index = index
                fuz_title = num[0]
                fuz_choose = num[1]
                fuz_answer_num = num[2]
                break
            elif title not in self.duplicate_title and title == num[0]:  # 标题不在重复列表中的，标题一样就算匹配到了
                fuz_index = index
                fuz_title = num[0]
                fuz_choose = num[1]
                fuz_answer_num = num[2]
                break
        new_title_sign = 0  # 新标题标记
        if fuz_title is None:  # 没有匹配到
            print('*****没有匹配到题目', title, answer, '记录下来，答案预先设为ABCD')
            data_ti_ku.append([title, answer, 'ABCD'])
        elif fuz_choose != answer:  # 找到了和原来题目一样，但是选项不一样的题
            print(f'*****找到题目和存储的一样***{title}-{fuz_title}***，但是选项{fuz_choose}-{answer}不一样')
            data_ti_ku.append([title, answer, 'ABCD'])
            self.duplicate_title.append(fuz_title)
            self.duplicate_title = list(set(self.duplicate_title))
        else:  # 匹配到了
            # print('匹配到了', fuz_title, answer, '匹配的答案是', fuz_answer_num)
            if len(fuz_answer_num) > 1:
                new_title_sign = 1
                print('新加入的题匹配到了', fuz_title, answer, '匹配的答案是', fuz_answer_num)
            if 'A' in fuz_answer_num:
                self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                              'android.view.View').all()[0].click()
                if fuz_answer_num == 'ABCD':
                    for k in range(4):
                        img_a = self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                                              'android.view.View').all()[k].screenshot()
                        r, g, b = img_a.resize((1, 1)).getpixel((0, 0))
                        if 230 > g > 150 > b > 100 > r > 50:
                            fuz_answer_num = 'ABCD'[k]
                            print(title, answer, fuz_answer_num)
                            break
            elif 'B' in fuz_answer_num:
                self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                              'android.view.View').all()[1].click()
                if fuz_answer_num == 'ABCD':
                    for k in range(4):
                        img_a = self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                                              'android.view.View').all()[k].screenshot()
                        r, g, b = img_a.resize((1, 1)).getpixel((0, 0))
                        if 230 > g > 150 > b > 100 > r > 50:
                            fuz_answer_num = 'ABCD'[k]
                            print(title, answer, fuz_answer_num)
                            break
            elif 'C' in fuz_answer_num:
                self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                              'android.view.View').all()[2].click()
                if fuz_answer_num == 'ABCD':
                    for k in range(4):
                        img_a = self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                                              'android.view.View').all()[k].screenshot()
                        r, g, b = img_a.resize((1, 1)).getpixel((0, 0))
                        if 230 > g > 150 > b > 100 > r > 50:
                            fuz_answer_num = 'ABCD'[k]
                            print(title, answer, fuz_answer_num)
                            break
            elif 'D' in fuz_answer_num:
                self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                              'android.view.View').all()[3].click()
                if fuz_answer_num == 'ABCD':
                    for k in range(4):
                        img_a = self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View/'
                                              'android.view.View').all()[k].screenshot()
                        r, g, b = img_a.resize((1, 1)).getpixel((0, 0))
                        if 230 > g > 150 > b > 100 > r > 50:
                            fuz_answer_num = 'ABCD'[k]
                            print(title, answer, fuz_answer_num)
                            break
            else:
                print(f'{fuz_title}在记录中没有正确答案,')
                fuz_answer_num = 'ABCD'
            dui_num = 0
            try:  # 获取连续做对题的数目，然后返回结果
                dui_num = self.pp.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/'
                                        'android.view.View[1]/android.view.View[1]/android.view.View[1]/'
                                        'android.view.View[1]/android.view.View').get(timeout=0.1)
                dui_num = int(re.search(r'连续答对X(\d*)', dui_num.text).group(1))
            except uiautomator2.exceptions.XPathElementNotFoundError:
                pass
            data_ti_ku[fuz_index] = [fuz_title, fuz_choose, fuz_answer_num]  # 只要匹配到题了，就更新下题目和答案以及选项
            if new_title_sign == 1:  # 如果是新标题的题，就保存一下
                with open(os.path.join(self.path, 'ti_ku_verify.json'), 'w', encoding='UTF-8') as f2:
                    json.dump(data_ti_ku, f2, ensure_ascii=False, indent=2)
            time.sleep(1)
            if self.pp(text="结束本局").exists or self.pp(text="再来一局").exists:
                print(f'{fuz_title}, {fuz_choose}, {fuz_answer_num}', '找到题了，但是答错了，请核实答案')
            return dui_num

    def run_tiao_zhan(self, ti_num=10):
        time.sleep(1)
        self.pp(text='我要答题').wait()
        self.pp(text='我要答题').click()
        self.pp(text='挑战答题').wait()
        self.pp(text='挑战答题').click()
        with open(os.path.join(self.path, 'ti_ku_verify.json'), 'r', encoding="UTF-8") as f1:
            data_ti_ku = json.load(f1)
        for ij, j1 in enumerate(data_ti_ku):
            for ik, k in enumerate(data_ti_ku):
                if j1[0] == k[0] and ij != ik:
                    self.duplicate_title.append(j1[0])
        self.duplicate_title = list(set(self.duplicate_title))
        dui_num = 0
        while True:
            try:
                temp = self.do_tiao_zhan_ti(data_ti_ku)
                if temp:
                    dui_num = temp
                # print('已经连续做对{}道挑战答题的题'.format(dui_num))
            except uiautomator2.exceptions.UiObjectNotFoundError:
                pass
            except uiautomator2.exceptions.XPathElementNotFoundError:
                pass
            # except Exception as e:
            #     print(e)
            if dui_num >= ti_num:
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
        # ti_shi_pic.show()
        # ti_shi_pic.save(f'{random.random()}.png')
        for p in range(pic_text_num):  # 识别，把不是红色的地方都变白色。
            img = ti_shi_pic.crop((0, int(height / pic_text_num * p), width, int(height / pic_text_num * (p + 1))))
            for w in range(width):
                for h in range(int(height / pic_text_num)):
                    color = img.getpixel((w, h))
                    if color[0] > 150 and color[1] < 140 and color[2] < 140:
                        img.putpixel((w, h), (0, 0, 0))
                    else:
                        img.putpixel((w, h), (255, 255, 255))
            # img.resize((img.size[0]*5, img.size[1]*5))
            # img.show()
            # img.save(f'{random.random()}.png')
            # print(img.size)
            pic_str = pytesseract.image_to_string(img, lang='chi_sim')
            # pic_str = pytesseract.image_to_boxes(img, lang='chi_sim')
            # print(pic_str)
            pic_str = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(pic_str).replace('\xa0', '').replace('_', ''))
            # print(pic_str)
            # if not pic_str:
            #     img.save(f'{split_height} {kuai_num}.png')
            # print(pic_str)
            ti_shi_word += pic_str
        return ti_shi_word

    @staticmethod
    def video_to_text():
        return 'wwo le qu ge ren a ha ah'

    def do_everyday_ti(self):
        # 获取题的类型
        self.pp.xpath('//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]'
                      '/android.view.View[1]/android.view.View[1]/android.view.View').wait()
        ti_type = self.pp.xpath('//*[@resource-id="app"]/android.view.View[2]/android.view.View[1]'
                                '/android.view.View[1]/android.view.View[1]/android.view.View').get_text()
        self.pp(scrollable=True).scroll.toEnd()
        self.pp(text='查看提示').wait()
        self.pp(text='查看提示').click()
        time.sleep(1)
        ti_shi = self.pp.xpath('//*[@resource-id="app"]/android.view.View[2]/android.view.View[3]'
                               '/android.view.View[2]/android.view.View').get_text()
        ti_shi = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(ti_shi).replace('\xa0', '').replace('_', ''))
        ti_shi_pic = self.pp.xpath('//*[@resource-id="app"]/android.view.View[2]/android.view.View[3]'
                                   '/android.view.View[2]/android.view.View').screenshot()
        self.pp.press('back')
        time.sleep(1)
        self.pp(scrollable=True).scroll.toBeginning()
        if ti_type == '填空题':
            # 看下是不是视频题
            if not self.pp.xpath('//android.widget.Image').exists:
                ti_shi_word = self.pic_to_text(ti_shi_pic)
            else:  # 是视频题
                ti_shi_word = 'salkdjf;alksdjf'
            if ti_shi_word not in ti_shi:
                print(f'在提示\n{ti_shi}\n中识别出来的红色关键词\n{ti_shi_word}\n不匹配')
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
        else:  # 选择题
            ti_shi_word = ti_shi
            answer = []
            for choose in self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View[1]'
                                        '/android.view.View[2]').all():
                answer_clean = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(choose.text).replace('\xa0', '').replace('_', ''))
                answer.append(choose.text)
                if answer_clean in ti_shi_word:
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
                if job_sta[5][0] == '已完成':
                    break
                time.sleep(1)
                self.pp(text='我要答题').wait()
                self.pp(text='我要答题').click()
                self.pp(text='每日答题').wait()
                self.pp(text='每日答题').click()
                time.sleep(1)

    def read_issue(self, job_temp, test=False):
        need_issue_num = int(job_temp[2][2]) - int(job_temp[2][1])
        need_share_num = 2 - int(job_temp[11][1])
        need_collection_num = 2 - int(job_temp[10][1])
        need_comment_num = int(job_temp[12][2]) - int(job_temp[12][1])
        need_time_num = int(job_temp[3][2]) - int(job_temp[3][1])
        try:
            with open(os.path.join(self.path, f'data_issue_{self.learn_num}.json'), 'r', encoding="UTF-8") as f1:
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
            for ci_shu in range(8):  # 每个栏目下滑8次页面找文章看
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
                        print(f'{t.text} 第{isu+1}个文章标题获取出错，跳过')
                        continue
                    if title in data_issue:
                        self.pp.press('back')
                        print(f'{t.text} {title}  已经看过了，跳过')
                        continue
                    print('正在看', t.text, title)
                    need_issue_num -= 1
                    data_issue.append(title)
                    with open(os.path.join(self.path, f'data_issue_{self.learn_num}.json'),
                              'w', encoding='UTF-8') as f2:
                        json.dump(data_issue, f2, ensure_ascii=False, indent=2)
                    time.sleep(10)  # 每个文章学习七秒
                    if job_temp[3][0] != '已完成' and need_time_num > 0:  # 如果没有完成文章学习时长任务，就开始
                        t1 = time.time()
                        while True:
                            if time.time() - t1 > 110:
                                break
                            self.pp(scrollable=True).scroll.vert.forward(steps=random.randint(130, 150))
                            time.sleep(1)
                            self.pp(scrollable=True).scroll.vert.backward(steps=random.randint(110, 130))
                            time.sleep(1)
                        need_time_num -= 1
                    if job_temp[10][0] != '已完成' and need_collection_num > 0:  # 如果没有完成收藏任务，就开始
                        self.pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                                      f'/android.widget.ImageView[1]').wait()  # 收藏
                        self.pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                                      f'/android.widget.ImageView[1]').click()  # 收藏
                        time.sleep(1)
                        if self.pp(text='我知道了').exists:
                            self.pp(text='我知道了').click()
                            time.sleep(1)
                        need_collection_num -= 1
                    if job_temp[11][0] != '已完成' and need_share_num > 0:  # 如果没有完成分享任务，就分享及返回
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
                        need_share_num -= 1
                    if job_temp[12][0] != '已完成' and need_comment_num > 0:  # 如果没有完成评论任务，就开始评论，之后删除评论
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
                        need_comment_num -= 1
                    self.pp.press('back')  # 学习完每一篇文章后返回
                    time.sleep(1)
                    if not test and need_issue_num <= 0:
                        self.pp(text='我的').must_wait()
                        self.pp.xpath(
                            '//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click()  # 点击积分,查一下积分完成情况
                        job_temp = self.job_status()  # 查一下积分完成情况
                        need_issue_num = int(job_temp[2][2]) - int(job_temp[2][1])
                        need_share_num = 2 - int(job_temp[11][1])
                        need_collection_num = 2 - int(job_temp[10][1])
                        need_comment_num = int(job_temp[12][2]) - int(job_temp[12][1])
                        need_time_num = int(job_temp[3][2]) - int(job_temp[3][1])
                        if job_temp[1][0] == '已完成':  # 如果学习文章没完成，就开始学习
                            self.pp(text='我的').wait()
                            self.pp(text='我的').click()
                            print('阅读文章任务已完成')
                            return
                time.sleep(1)
                if it == 0:  # 为了跳过推荐频道里的本地新闻栏目，避免错误点击到
                    self.pp(scrollable=True).scroll.toEnd(steps=90, max_swipes=4)
                else:
                    self.pp(scrollable=True).scroll(steps=90)
                time.sleep(1)

    def read_video(self, job_temp, test=False):
        need_video_num = int(job_temp[2][2]) - int(job_temp[2][1])
        try:
            with open(os.path.join(self.path, f'data_video_{self.learn_num}.json'), 'r', encoding="UTF-8") as f1:
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
            for ci_shu in range(8):  # 向下滑动8次页面
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
                    need_video_num -= 1
                    data_video.append(title)
                    with open(os.path.join(self.path, f'data_video_{self.learn_num}.json'),
                              'w', encoding='UTF-8') as f2:
                        json.dump(data_video, f2, ensure_ascii=False, indent=2)
                    time.sleep(1)  # 每个视频学习10秒
                    if self.pp(text='继续播放').exists:
                        self.pp(text='继续播放').click()
                    time.sleep(9)  # 每个视频学习10秒
                    # if job_temp[4][0] != '已完成':  # 如果没有完成视频学习时长任务，就开始，改成学习视频时长用看电视的方法，
                    #     t1 = time.time()
                    #     while True:
                    #         if time.time() - t1 > 180:
                    #             break
                    #         self.pp(text='点赞').click()
                    #         time.sleep(1)
                    self.pp.press('back')  # 学习完每一个视频后返回
                    time.sleep(1)
                    if not test and need_video_num <= 0:
                        self.pp(text='我的').wait()
                        self.pp.xpath(
                            '//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click()  # 点击积分,查一下积分完成情况
                        job_temp = self.job_status()  # 查一下积分完成情况
                        need_video_num = int(job_temp[2][2]) - int(job_temp[2][1])
                        time.sleep(1)
                        if job_temp[2][0] == '已完成':  # 如果学习视频没完成，就开始学习
                            time.sleep(1)
                            self.pp(text='我的').wait()
                            self.pp(text='我的').click()
                            print('看视频任务已完成')
                            return
                time.sleep(1)
                self.pp(scrollable=True).scroll(steps=90)
                time.sleep(1)

    def look_tel(self, job_temp):  # 看电视台的视频，主要是用来弥补视频学习时长
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
            if self.pp(text='点击播放').exists:
                self.pp(text='点击播放').click()
            t1 = time.time()
            while True:
                if time.time() - t1 > 180 * (int(job_temp[4][2]) - int(job_temp[4][1])):
                    break
                self.pp.screen_on()
                time.sleep(1)
            self.pp(text='我的').wait()
            self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click()  # 点击积分,查一下积分完成情况
            job_temp = self.job_status()  # 查一下积分完成情况
            time.sleep(1)
            if job_temp[4][0] == '已完成':  # 如果视频学习时长任务没完成，就开始学习
                self.pp(text='我的').wait()
                self.pp(text='我的').click()
                print('看视频任务已完成')
                return

    def listen_tai_start(self):  # 听电台的音频开始程序，主要是用来弥补视频学习时长
        time.sleep(1)
        self.pp.press('back')  # 从我的界面回到app首页
        time.sleep(1)
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_mine"]').wait()  # 点击首页下面的电台按钮
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_mine"]').click()
        time.sleep(1)
        self.pp(text='听新闻广播').wait()
        self.pp(text='听新闻广播').click()
        time.sleep(1)
        if not self.pp.xpath('//android.support.v4.view.ViewPager[1]/android.support.v7.widget.RecyclerView[1]'
                             '/android.widget.FrameLayout[1]').exists:
            self.pp(scrollable=True).scroll(steps=90)
            time.sleep(1)
        try:
            self.pp.xpath('//android.support.v4.view.ViewPager[1]/android.support.v7.widget.RecyclerView[1]'
                          '/android.widget.FrameLayout[1]').click()
        except uiautomator2.exceptions.XPathElementNotFoundError:
            print('找不到中国之声电台，不能播放')
            return
        time.sleep(1)
        self.pp(text='我的').wait()
        self.pp(text='我的').click()
        return time.time()

    def listen_tai_end(self, job_temp, t):  # 听电台的音频结束程序，主要是用来弥补视频学习时长
        t2 = time.time()
        if t2 - t > 180 * (int(job_temp[4][2]) - int(job_temp[4][1])):
            pass
        else:
            while True:
                if time.time() - t > 180 * (int(job_temp[4][2]) - int(job_temp[4][1])):
                    break
                time.sleep(1)
                self.pp.screen_on()
        if self.pp.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                         'android.widget.FrameLayout[1]').exists:
            self.pp.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                          'android.widget.FrameLayout[1]').click()
            time.sleep(1)
            self.pp.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                          'android.widget.FrameLayout[1]/android.widget.ImageView[4]').click()
        else:
            print('就没有打开收听电台的小栏目，只能重新看了')
            return
        if self.pp(text='我的').exists:
            self.pp(text='我的').click()
        time.sleep(1)

    def do_ding_yue(self):
        time.sleep(1)
        self.pp(text='订阅').wait()
        self.pp(text='订阅').click()
        time.sleep(1)
        self.pp(text='添加').wait()
        self.pp(text='添加').click()
        time.sleep(1)
        while True:
            if self.pp(description="订阅").count < 2:
                self.pp(scrollable=True).scroll(steps=150)
                time.sleep(1)
            else:
                break
            if self.pp(text='你已经看到我的底线了').exists:
                break
        for i in range(2):
            if self.pp(description="订阅").exists:
                self.pp(description="订阅").click()
            time.sleep(1)
        if self.pp(text='你已经看到我的底线了').exists:
            return False
        self.pp.press("back")
        self.pp(text='我的订阅').wait()
        self.pp.press("back")
        return True

    def run_ding_yue(self, job_stat):
        while True:
            if job_stat[9][0] != '已完成':
                res = self.do_ding_yue()
                if not res:
                    break
                time.sleep(1)
                self.pp(text='学习积分').wait()
                self.pp(text='学习积分').click()
                job_stat = self.job_status()
            else:
                break

    def ben_di(self):
        time.sleep(1)
        self.pp.press("back")
        time.sleep(1)
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').wait()  # 点击首页下面的学习按钮
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').click()
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
            com = self.pp.xpath(f'//android.widget.ListView/android.view.View[{j}]/android.view.View[3]').get_text()
            com1, com2 = re.search(r'已获(\d*)分/每日上限(\d*)分', com).groups()
            sta = self.pp.xpath(f'//android.widget.ListView/android.view.View[{j}]/android.view.View[4]').get_text()
            job_status1.append((sta, com1, com2))
        self.pp.press('back')  # 查一下积分完成情况
        time.sleep(1)
        return job_status1

    def get_learn_num(self):
        self.pp(description='我的信息').wait()
        self.pp(description='我的信息').click()
        time.sleep(1)
        learn_num = self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/user_info_fragment_container"]'
                                  '/android.widget.LinearLayout[3]/android.widget.LinearLayout[1]'
                                  '/android.widget.TextView[2]').get_text()
        print('这个手机学习强国的学号是', learn_num)
        self.pp.press('back')
        time.sleep(1)
        return learn_num

    def main_do(self, test=False):  # 主运行程序
        self.pp.unlock()
        if test:
            self.test_pro()
        if 'cn.xuexi.android' in self.pp.app_list_running():
            self.pp.app_stop('cn.xuexi.android')
        self.pp.app_start('cn.xuexi.android')
        self.pp(text='我的').wait()
        self.pp(text='我的').click()
        time.sleep(1)
        self.learn_num = self.get_learn_num()
        self.pp(text='学习积分').wait()
        self.pp(text='学习积分').click()
        self.pp(text='积分规则').wait()
        job_stat = self.job_status()
        self.pp(text='我的').wait()
        if job_stat[2][0] != '已完成':
            self.read_video(job_stat)
        else:
            print('已完成视频观看')
        if job_stat[4][0] != '已完成':
            t = self.listen_tai_start()
        else:
            t = 0
            print('已完成视听时长学习')
        if job_stat[9][0] != '已完成':
            self.run_ding_yue(job_stat)
        else:
            print('已完成订阅')
        if job_stat[13][0] != '已完成':
            self.ben_di()
        else:
            print('已完成本地频道')
        if job_stat[1][0] != '已完成':
            self.read_issue(job_stat)
        else:
            print('已完成文章阅读')
        if job_stat[5][0] != '已完成':
            self.run_everyday_ti()
        else:
            print('已完成每日答题任务')
        if job_stat[8][0] != '已完成':
            self.run_tiao_zhan()
        else:
            print('已完成挑战答题')
        if job_stat[4][0] != '已完成' and t:
            self.listen_tai_end(job_stat, t)
        else:
            print('已完成视听时长学习')
        # if job_stat[4][0] != '已完成':
        #     self.look_tel(job_stat)
        # else:
        #     print('已完成视听时长学习')
        self.pp(text='学习积分').click()
        self.__del__()

    def test_pro(self):  # 测试专用程序
        self.pp.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                      'android.widget.FrameLayout[1]').click()
        time.sleep(1)
        self.pp.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                      'android.widget.FrameLayout[1]/android.widget.ImageView[4]').click()
        # print(self.pp.dump_hierarchy())
        # self.run_everyday_ti()
        # self.run_tiao_zhan(ti_num=9999)
        # self.listen_tai_start()
        # self.listen_tai_end()
        raise ()


if __name__ == '__main__':
    # 要在对象创建时传入参数tesseract_path，表示pytesseract.pytesseract.tesseract_cmd的路径，
    # 否则使用默认值r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    do = QiangGuoFuZhu()
    # do.main_do(test=True)
    do.main_do()
