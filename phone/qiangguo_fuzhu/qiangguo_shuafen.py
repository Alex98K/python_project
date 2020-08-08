import json
import os
import random
import re
import time
import pytesseract
import uiautomator2
from fuzzywuzzy import process
from down_ti_ku import DownTiKu


class QiangGuoFuZhu(object):
    def __init__(self, username=None, password=None, unlock_password=None,
                 tesseract_path=r'C:/Program Files/Tesseract-OCR/tesseract.exe'):
        super(QiangGuoFuZhu, self).__init__()
        self.path = os.path.abspath(os.path.dirname(__file__))
        if os.name != 'posix':
            pytesseract.pytesseract.tesseract_cmd = tesseract_path  # tesseract可执行文件的路径
        self.pp = self.connect_phone_usb()
        # self.pp = uiautomator2.connect_wifi('192.168.1.218')
        # self.pp = uiautomator2.connect('127.0.0.1:62001')
        self.duplicate_title = []
        self.learn_num = None
        self.username = username
        self.password = password
        self.unlock_password = unlock_password
        # 注册watcher，如果顶部的快捷栏被无意间滑下来了，就自动返回，划上去
        self.pp.watcher('notification').when(xpath="//*[@resource-id='com.android.systemui:id"
                                                   "/notification_container_parent']").call(self.call_back)
        self.pp.watcher('fresh1').when('刷新').click()
        self.pp.watcher('fresh2').when('网络开小差～请稍后试试').when('确定').click()
        self.pp.watcher.start(0.2)

    def __del__(self):
        try:
            self.pp.watcher.stop()
            self.pp.watcher.remove()
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

    def do_challenge_ti(self, data_ti_ku):  # 挑战答题主程序，用来做一个题
        if self.pp(text="结束本局").click_exists():
            self.pp(text='再来一局').click(timeout=2)
        self.pp(text='再来一局').click_exists()
        if self.pp(text="选择联系人").exists:
            self.pp(description="返回").click_exists()
        # self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/android.view.View[3]/android.view.View['
        #               '1]/android.view.View[1]/android.view.View[1]').wait()
        title = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/android.view.View[3]/'
                              'android.view.View[1]/android.view.View[2]/android.view.View[1]/'
                              'android.view.View[1]').get(timeout=20).text  # 匹配标题
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
                # print('新加入的题匹配到了', fuz_title, answer, '匹配的答案是', fuz_answer_num)
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
                            print(title, answer, '正确答案是', fuz_answer_num)
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
                            print(title, answer, '正确答案是', fuz_answer_num)
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
                            print(title, answer, '正确答案是', fuz_answer_num)
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
                            print(title, answer, '正确答案是', fuz_answer_num)
                            break
            else:
                print(f'{fuz_title}在记录中没有正确答案,')
                fuz_answer_num = 'ABCD'
            dui_num = 0
            try:  # 获取连续做对题的数目，然后返回结果
                dui_num = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                                        'android.view.View[3]/android.view.View[1]/android.view.View[1]/'
                                        'android.view.View[1]/android.view.View[1]/android.view.View').get(timeout=0.1)
                dui_num = int(re.search(r'连续答对X(\d*)', dui_num.text).group(1))
            except uiautomator2.exceptions.XPathElementNotFoundError:
                pass
            data_ti_ku[fuz_index] = [fuz_title, fuz_choose, fuz_answer_num]  # 只要匹配到题了，就更新下题目和答案以及选项
            if new_title_sign == 1:  # 如果是新标题的题，就保存一下
                with open(os.path.join(self.path, 'ti_ku_verify.json'), 'w', encoding='UTF-8') as f2:
                    json.dump(data_ti_ku, f2, ensure_ascii=False, indent=2)
            time.sleep(1)
            if (self.pp(text="结束本局").exists or self.pp(text="再来一局").exists) and new_title_sign == 0:
                print(f'{fuz_title}, {fuz_choose}, {fuz_answer_num}', '找到旧题了，但是答错了，请核实答案')
            return dui_num

    def run_challenge(self, ti_num=10):
        self.pp(text='我要答题').click(timeout=20)
        self.pp(text='挑战答题').click(timeout=20)
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
                temp = self.do_challenge_ti(data_ti_ku)
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
                self.pp(text='结束本局').click(timeout=40)
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
            pic_str = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(pic_str).replace('\xa0', '').replace('_', ''))
            ti_shi_word += pic_str
        return ti_shi_word

    @staticmethod
    def video_to_text():
        return 'wwo le qu ge ren a ha ah'

    def _do_day_week_special_backup(self, ti_type):
        self.pp(scrollable=True).scroll.toEnd()
        self.pp(text='查看提示').click(timeout=20)
        time.sleep(1)
        ti_shi = self.pp.xpath('//*[@text="提示"]/../following-sibling::android.view.View/android.view.View').get(
            timeout=20).text
        ti_shi = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(ti_shi).replace('\xa0', '').replace('_', ''))
        ti_shi_pic = self.pp.xpath(
            '//*[@text="提示"]/../following-sibling::android.view.View/android.view.View').screenshot()
        self.pp.press('back')
        time.sleep(1)
        self.pp(scrollable=True).scroll.toBeginning()
        if ti_type == '填空题':
            # 看下是不是视频题
            if not self.pp.xpath('//android.widget.Image').exists:
                ti_shi_word = self.pic_to_text(ti_shi_pic)
            else:  # 是视频题
                ti_shi_word = '重大决策保障机制'
            if ti_shi_word not in ti_shi:
                print(f'在提示\n{ti_shi}\n中识别出来的红色关键词\n{ti_shi_word}\n不匹配')
            # 根据有多少个填空区域进行填空
            if self.pp(className='android.widget.EditText').count == 1:
                self.pp.xpath('//android.widget.EditText/../android.view.View[1]').set_text(ti_shi_word)
            else:
                # 遍历每个填空区域
                for pp1 in self.pp.xpath('//android.widget.EditText/../android.view.View[1]').all():
                    # 获取每个填空区域有几个空格
                    text_len = len(self.pp.xpath(str(pp1.get_xpath()) + '/..//android.view.View').all())
                    # 给每个填空区域填空
                    self.pp.xpath(pp1.get_xpath()).set_text(ti_shi_word)
                    # 删除已经填了空的
                    ti_shi_word = ti_shi_word.replace(ti_shi_word[:text_len], '')
                    # print(ti_shi_word, ti_shi_word_temp)
            time.sleep(2)
            if self.pp(text='确定').exists or self.pp(text='下一题').exists or self.pp(text='完成').exists:
                self.pp(text='确定').click_exists(timeout=2)
                self.pp(text='下一题').click_exists(timeout=2)
                self.pp(text='完成').click_exists(timeout=2)
            else:
                print('没找到完全匹配的答案，随便填写了')
                for j in self.pp.xpath('//android.widget.EditText/../android.view.View[1]').all():
                    self.pp.xpath(j.get_xpath()).set_text('重大机制保障机制')
                time.sleep(2)
                if not (self.pp(text='确定').exists or self.pp(text='下一题').exists or self.pp(text='完成').exists
                        or self.pp(text='再来一次').exists):
                    print('这个填空题没法自动答题，手动答题吧')
                    raise
                else:
                    self.pp(text='确定').click_exists(timeout=2)
                    self.pp(text='下一题').click_exists(timeout=2)
                    self.pp(text='完成').click_exists(timeout=2)
        else:  # 选择题
            ti_shi_word = ti_shi
            answer = []
            for choose in self.pp.xpath('//android.widget.ListView//android.view.View/android.view.View[1]'
                                        '/android.view.View[2]').all():
                answer_clean = re.sub(r'[^\w\u4e00-\u9fa5]', '',
                                      str(choose.text).replace('\xa0', '').replace('_', ''))
                answer.append(choose.text)
                if answer_clean in ti_shi_word:
                    choose.click()
            time.sleep(1)
            if self.pp(text='确定').exists or self.pp(text='下一题').exists or self.pp(text='完成').exists:
                self.pp(text='确定').click_exists(timeout=2)
                self.pp(text='下一题').click_exists(timeout=2)
                self.pp(text='完成').click_exists(timeout=2)
            else:
                # print('没找到完全匹配的答案，找个最合适的')
                da_an = str(process.extractOne(ti_shi_word, answer)[0])
                self.pp(text=da_an).click()
                time.sleep(1)
                if not (self.pp(text='确定').exists or self.pp(text='下一题').exists or self.pp(text='完成').exists
                        or self.pp(text='再来一次').exists):
                    print('这个选择题没法自动答题，手动答题吧')
                    raise
                else:
                    self.pp(text='确定').click_exists(timeout=2)
                    self.pp(text='下一题').click_exists(timeout=2)
                    self.pp(text='完成').click_exists(timeout=2)

    def do_everyday_ti(self):
        # 获取题的类型
        ti_type = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[2]/'
                                'android.view.View[1]/android.view.View[1]/android.view.View[1]/'
                                'android.view.View').get(timeout=20).text
        self._do_day_week_special_backup(ti_type)

    def run_everyday_ti(self):
        time.sleep(1)
        self.pp(text='我要答题').click(timeout=20)
        self.pp(text='知道了').click_exists(timeout=5)
        self.pp(text='每日答题').click(timeout=20)
        time.sleep(1)
        while True:
            self.do_everyday_ti()
            time.sleep(1)
            if self.pp(text='再来一组').exists:
                self.pp(text='返回').click_gone()
                self.pp.press('back')
                time.sleep(1)
                self.pp(text='学习积分').click(timeout=20)
                time.sleep(1)
                job_sta = self.job_status()
                if job_sta[5][0] == '已完成':
                    break
                time.sleep(1)
                self.pp(text='我要答题').click(timeout=20)
                self.pp(text='每日答题').click(timeout=20)
                time.sleep(1)

    def do_week_and_special_ti(self, answer, every_ti_num):
        time.sleep(1)
        self.pp(text='加载中...').wait_gone()
        # 获取题的序数
        ti_num = -1
        for i in range(10):
            if self.pp(text=f'{i + 1} /{every_ti_num}').exists:
                ti_num = i
                break
        ti_shi_word = answer[ti_num]
        # 获取题的类型
        ti_type = self.pp(text=f'{ti_num + 1} /{every_ti_num}').sibling(className='android.view.View').get_text()[:3]
        if not ti_type:
            print('没有找到题目类型，出错')
            raise
        if (ti_type == '多选题' or ti_type == '单选题' or ti_type == '判断题') and (('A' in ti_shi_word and not self.pp.xpath(
                '//android.widget.ListView/android.view.View[1]/android.view.View[1]').exists
                or 'B' in ti_shi_word and not self.pp.xpath('//android.widget.ListView/android.view.View[2]/'
                                                            'android.view.View[1]').exists
                or 'C' in ti_shi_word and not self.pp.xpath('//android.widget.ListView/android.view.View[3]/'
                                                            'android.view.View[1]').exists
                or 'D' in ti_shi_word and not self.pp.xpath('//android.widget.ListView/android.view.View[4]/'
                                                            'android.view.View[1]').exists)
                or ('A' not in ti_shi_word and 'B' not in ti_shi_word and 'C' not in ti_shi_word
                    and 'D' not in ti_shi_word)) \
                or (ti_type == '填空题' and ('A' in ti_shi_word or 'B' in ti_shi_word
                                          or 'C' in ti_shi_word or 'D' in ti_shi_word)):
            print(ti_shi_word, '答案有问题，请查错')
            return False
        if ti_type == '填空题':
            if self.pp(className='android.widget.EditText').count == 1:
                self.pp.xpath('//android.widget.EditText/../android.view.View[1]').set_text(ti_shi_word)
            else:
                # 遍历每个填空区域
                for pp1 in self.pp.xpath('//android.widget.EditText/../android.view.View[1]').all():
                    # 获取每个填空区域有几个空格
                    text_len = len(self.pp.xpath(str(pp1.get_xpath()) + '/..//android.view.View').all())
                    # 给每个填空区域填空
                    self.pp.xpath(pp1.get_xpath()).set_text(ti_shi_word)
                    # 删除已经填了空的
                    ti_shi_word = ti_shi_word.replace(ti_shi_word[:text_len], '')
                    # print(ti_shi_word, ti_shi_word_temp)
            time.sleep(1)
            if self.pp(text='确定').exists:
                self.pp(text='确定').click()
                time.sleep(1)
                self.pp(text='下一题').click_exists()
                self.pp(text='完成').click_exists()
            elif self.pp(text='下一题').exists:
                self.pp(text='下一题').click()
            elif self.pp(text='完成').exists:
                self.pp(text='完成').click()
            else:
                print(ti_shi_word, '答案有问题，请查错')
                return False
        else:  # 选择题
            self.pp(scrollable=True).scroll.toEnd()
            try:
                if 'A' in ti_shi_word:
                    self.pp.xpath('//android.widget.ListView/android.view.View[1]/android.view.View[1]')\
                        .click(timeout=1)
                if 'B' in ti_shi_word:
                    self.pp.xpath('//android.widget.ListView/android.view.View[2]/android.view.View[1]')\
                        .click(timeout=1)
                if 'C' in ti_shi_word:
                    self.pp.xpath('//android.widget.ListView/android.view.View[3]/android.view.View[1]')\
                        .click(timeout=1)
                if 'D' in ti_shi_word:
                    self.pp.xpath('//android.widget.ListView/android.view.View[4]/android.view.View[1]')\
                        .click(timeout=1)
            except uiautomator2.exceptions.XPathElementNotFoundError:
                print(ti_shi_word, '答案有问题，请查错')
                return False
            time.sleep(1)
            if self.pp(text='确定').exists:
                self.pp(text='确定').click()
                time.sleep(1)
                self.pp(text='下一题').click_exists()
                self.pp(text='完成').click_exists()
            elif self.pp(text='下一题').exists:
                self.pp(text='下一题').click()
            elif self.pp(text='完成').exists:
                self.pp(text='完成').click()
            else:
                print(ti_shi_word, '答案有问题，请查错')
                return False
        return True

    def do_week_special_backup(self, every_ti_num):
        time.sleep(1)
        # 获取题的序数
        ti_num = -1
        for i in range(10):
            if self.pp(text=f'{i + 1} /{every_ti_num}').exists:
                ti_num = i
                break
        # 获取题的类型
        ti_type = self.pp(text=f'{ti_num + 1} /{every_ti_num}').sibling(className='android.view.View').get_text()[:3]
        self._do_day_week_special_backup(ti_type)

    def run_every_week_ti(self, fuck=False, test=False):
        with open(os.path.join(self.path, f'mei_zhou.json'), 'r', encoding="UTF-8") as f2:
            week_ti_all = json.load(f2)
        time.sleep(1)
        self.pp(text='我要答题').click(timeout=20)
        self.pp(text='知道了').click_exists(timeout=5)
        self.pp(text='每周答题').click(timeout=20)
        time.sleep(1)
        self.pp(text='加载中...').wait_gone()
        top_y = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                              'android.view.View[1]').get(timeout=5).bounds[3]
        down_y = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                               'android.view.View[2]').get(timeout=5).bounds[3]
        date_title = ''
        answer = []
        last_j_num = -1
        while True:
            break_sign = 0
            all_week_ti_xpath = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                                              'android.view.View[2]//android.widget.ListView/android.view.View').all()
            for j_num, j in enumerate(all_week_ti_xpath):
                if j_num <= last_j_num:
                    continue
                else:
                    last_j_num = j_num
                j_xpath = j.get_xpath()
                j_bounds = self.pp.xpath(j_xpath).get().bounds
                j_rect = self.pp.xpath(j_xpath).get().rect
                while j_rect[3] < 20 or j_bounds[1] < top_y:
                    if j_bounds[1] < top_y:
                        self.pp(scrollable=True).scroll.backward(steps=180)
                    elif j_bounds[1] > down_y - j_rect[3] - 1:
                        self.pp(scrollable=True).scroll(steps=180)
                    j_bounds = self.pp.xpath(j_xpath).get().bounds
                    j_rect = self.pp.xpath(j_xpath).get().rect
                j_status = self.pp.xpath(j_xpath + '/android.view.View[2]').get_text()
                if j_status == '未作答':
                    date_title = self.pp.xpath(j_xpath + '/android.view.View[1]').get_text()
                    date_title = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(date_title).replace('\xa0', '').replace('_', ''))
                    if '年' not in date_title:
                        date_title = '2018年' + date_title
                    try:
                        answer = week_ti_all[date_title]
                        self.pp.click(j_bounds[0] + 1, j_bounds[3] - 1)
                        print(f'开始做题-{date_title} 答案是 {answer}')
                    except KeyError:
                        print(f'{date_title}  题目在题库里没有答案')
                        if fuck:
                            self.pp.click(j_bounds[0] + 1, j_bounds[3] - 1)
                        else:
                            continue
                    while True:
                        time.sleep(1)
                        if not (answer and self.do_week_and_special_ti(answer, every_ti_num=5)):
                            answer = []
                            self.do_week_special_backup(every_ti_num=5)
                        time.sleep(1)
                        if self.pp(text='返回').exists:
                            self.pp(text='返回').click_gone()
                            self.pp.press('back')
                            time.sleep(1)
                            self.pp.press('back')
                            time.sleep(1)
                            self.pp(text='学习积分').click(timeout=20)
                            time.sleep(1)
                            job_sta = self.job_status()
                            if job_sta[6][0] == '已完成' and not test:
                                return
                            else:
                                time.sleep(1)
                                self.pp(text='我要答题').click_exists(timeout=20)
                                self.pp(text='每周答题').click_exists(timeout=20)
                                break_sign = 1
                                break
                if break_sign == 1:
                    break
            self.pp(scrollable=True).scroll(steps=90)
            print('下滑一次，打开下面的题目')
            if (self.pp(text='您已经看到了我的底线').exists and
                    down_y > self.pp(text='您已经看到了我的底线').bounds()[1] > top_y and
                    self.pp(text='您已经看到了我的底线').bounds()[3] - self.pp(text='您已经看到了我的底线').bounds()[1] > 5):
                print('到底了，没题目了，跳出')
                break
        if not date_title:
            print('没有获取到题目名称')
            raise

    def run_special_ti(self, fuck=False, test=False):
        with open(os.path.join(self.path, f'zhuan_xiang.json'), 'r', encoding="UTF-8") as f1:
            special_ti_all = json.load(f1)
        time.sleep(1)
        self.pp(text='我要答题').click(timeout=20)
        self.pp(text='知道了').click_exists(timeout=5)
        self.pp(text='专项答题').click(timeout=20)
        time.sleep(1)
        self.pp(text='加载中...').wait_gone()
        top_y = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                              'android.view.View[1]').get(timeout=5).bounds[3]
        down_y = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                               'android.view.View[2]').get(timeout=5).bounds[3]
        date_title = ''
        answer = []
        last_j_num = -1
        while True:
            break_sign = 0
            all_special_ti_xpath = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                                                 'android.view.View[2]//android.view.View/'
                                                 'android.view.View[last()]').all()
            for j_num, j in enumerate(all_special_ti_xpath):
                if j_num <= last_j_num:
                    continue
                else:
                    last_j_num = j_num
                j_xpath = j.get_xpath()
                j_bounds = self.pp.xpath(j_xpath).get().bounds
                j_rect = self.pp.xpath(j_xpath).get().rect
                while j_rect[3] < 20 or j_bounds[1] < top_y:
                    if j_bounds[1] < top_y:
                        self.pp(scrollable=True).scroll.backward(steps=180)
                    elif j_bounds[1] > down_y - j_rect[3] - 1:
                        self.pp(scrollable=True).scroll(steps=180)
                    j_bounds = self.pp.xpath(j_xpath).get().bounds
                    j_rect = self.pp.xpath(j_xpath).get().rect
                if j.text == '开始答题' or j.text == '继续答题' or j.text == '重新答题':
                    date_title = self.pp.xpath(j_xpath + '/../preceding-sibling::android.view.View[2]').get_text()
                    date_title = re.sub(r'[^\w\u4e00-\u9fa5]', '', str(date_title).replace('\xa0', '').replace('_', ''))
                    try:
                        answer = special_ti_all[date_title]
                        self.pp.click(j_bounds[0] + 1, j_bounds[3] - 1)
                        print(f'开始做题-{date_title} 答案是 {answer}')
                    except KeyError:
                        print(f'{date_title}  题目在题库里没有答案')
                        if fuck:
                            self.pp.click(j_bounds[0] + 1, j_bounds[3] - 1)
                        else:
                            continue
                    while True:
                        time.sleep(1)
                        if not (answer and self.do_week_and_special_ti(answer, every_ti_num=10)):
                            answer = []
                            self.do_week_special_backup(every_ti_num=10)
                        time.sleep(1)
                        if self.pp(text='查看解析').exists:
                            self.pp.press('back')
                            time.sleep(1)
                            self.pp.press('back')
                            time.sleep(1)
                            self.pp.press('back')
                            time.sleep(1)
                            self.pp(text='学习积分').click(timeout=20)
                            time.sleep(1)
                            job_sta = self.job_status()
                            if job_sta[7][0] == '已完成' and not test:
                                return
                            else:
                                time.sleep(1)
                                self.pp(text='我要答题').click(timeout=20)
                                self.pp(text='专项答题').click(timeout=20)
                                time.sleep(1)
                                break_sign = 1
                                break
                if break_sign == 1:
                    break
            self.pp(scrollable=True).scroll(steps=90)
            print('下滑一次，打开下面的题目')
            if (self.pp(text='您已经看到了我的底线').exists and
                    down_y > self.pp(text='您已经看到了我的底线').bounds()[1] > top_y and
                    self.pp(text='您已经看到了我的底线').bounds()[3] - self.pp(text='您已经看到了我的底线').bounds()[1] > 5):
                print('到底了，没题目了，跳出')
                break
        if not date_title:
            print('没有获取到题目名称')
            raise

    def read_issue(self, job_temp, test=False):
        need_issue_num = int(job_temp[1][2]) - int(job_temp[1][1])
        need_share_num = 2 - int(job_temp[11][1])
        need_collection_num = 2 - int(job_temp[10][1])
        need_comment_num = int(job_temp[12][2]) - int(job_temp[12][1])
        need_time_num = int(job_temp[3][2]) - int(job_temp[3][1])
        try:
            with open(os.path.join(self.path, f'data_issue_{self.learn_num}.json'), 'r', encoding="UTF-8") as f1:
                data_issue = json.load(f1)
        except FileNotFoundError:
            data_issue = []
        time.sleep(1)
        self.pp.press('back')  # 从我的界面回到app首页
        time.sleep(1)
        # 点击首页下面的中间学习按钮
        down_bounds = self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]') \
            .get(timeout=20).bounds
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').click(timeout=20)
        if issue_pin_dao := self.pp.xpath(
                '//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout[1]'
                '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]'
                '//android.widget.LinearLayout/android.widget.TextView').all():  # 获取文章分类列表
            top_bounds = self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/'
                                       'android.widget.FrameLayout[1]/android.widget.LinearLayout[1]//'
                                       'android.widget.LinearLayout[1]').get(timeout=3).bounds
        else:
            print('获取文章频道列表失败，请修改程序')
            raise
        for it, t in enumerate(issue_pin_dao):
            t.click()
            time.sleep(1)
            for ci_shu in range(8):  # 每个栏目下滑8次页面找文章看
                for isu, issue in enumerate(
                        self.pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout').all()):
                    # 跳过推荐栏目的全国学习平台以及包含打开文字的文章，不看
                    if self.pp.xpath(issue.get_xpath() + '//*[text="打开"]').exists:
                        continue
                    # 跳过推荐频道里的本地新闻栏目,该功能还不稳定，需要测试，如果不行就要把下面跳过的功能开启
                    # if not self.pp.xpath(issue.get_xpath() + '//android.widget.TextView').exists:
                    #     continue
                    if down_bounds[1] > issue.bounds[1] > top_bounds[3]:
                        self.pp.click((issue.bounds[0] + issue.bounds[2]) / 2, issue.bounds[1])
                    elif down_bounds[1] > issue.bounds[3] > top_bounds[3]:
                        self.pp.click((issue.bounds[0] + issue.bounds[2]) / 2, issue.bounds[3])
                    else:
                        continue
                    self.pp(text='我的').wait_gone(timeout=5)
                    if self.pp(text='我的').exists:
                        continue
                    try:
                        title = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                                              'android.view.View[1]/android.view.View[1]/android.view.View[2]/'
                                              'android.view.View[1]').get(timeout=10).text
                    except uiautomator2.exceptions.XPathElementNotFoundError:
                        if not self.pp(text='我的').exists:
                            self.pp.press('back')
                        print(f'{t.text} 第{isu + 1}个文章标题获取出错，跳过')
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
                                      f'/android.widget.ImageView[1]').click(timeout=20)  # 收藏
                        self.pp(text='我知道了').click_exists(timeout=1)
                        need_collection_num -= 1
                    if job_temp[11][0] != '已完成' and need_share_num > 0:  # 如果没有完成分享任务，就分享及返回
                        self.pp.xpath(f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                                      f'/android.widget.ImageView[2]').click(timeout=20)  # 分享
                        self.pp(text="分享到短信").click(timeout=20)
                        time.sleep(1)
                        while not self.pp.xpath(
                                f'//*[@resource-id="cn.xuexi.android:id/BOTTOM_LAYER_VIEW_ID"]'
                                f'/android.widget.ImageView[1]').exists:
                            self.pp.press('back')
                            time.sleep(1)
                            self.pp(resourceId="android:id/button1").click_exists()  # 点击放弃保存短信按钮
                        time.sleep(1)
                        need_share_num -= 1
                    if job_temp[12][0] != '已完成' and need_comment_num > 0:  # 如果没有完成评论任务，就开始评论，之后删除评论
                        self.pp(text="欢迎发表你的观点").click()  # 评论
                        self.pp(text="好观点将会被优先展示").wait()  # 评论
                        # self.pp(text="好观点将会被优先展示").set_text('支持，有希望了，加油，厉害了')  # 评论
                        self.pp.xpath('//*[@text="好观点将会被优先展示"]').set_text('支持，有希望了，加油，厉害了')
                        self.pp(text="发布").click(timeout=20)  # 评论
                        self.pp(text="删除").wait()  # 评论
                        while self.pp(text="删除").exists:
                            self.pp(text="删除").click()  # 评论
                            self.pp.xpath('//*[@resource-id="android:id/button1"]').click(timeout=20)
                            time.sleep(1)
                        need_comment_num -= 1
                    self.pp.press('back')  # 学习完每一篇文章后返回
                    time.sleep(1)
                    if not test and need_issue_num <= 0:
                        self.pp(text='我的').must_wait()
                        # 点击积分,查一下积分完成情况
                        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click(timeout=20)
                        job_temp = self.job_status()  # 查一下积分完成情况
                        need_issue_num = int(job_temp[1][2]) - int(job_temp[1][1])
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
                if it == 0 and ci_shu == 0:  # 为了跳过推荐频道里的本地新闻栏目，避免错误点击到
                    # continue
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
        # 点击首页下面的电视台按钮
        down_bounds = self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]') \
            .get(timeout=20).bounds
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').click(timeout=20)
        if video_pin_dao := self.pp.xpath(
                '//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout[1]'
                '/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]'
                '//android.widget.LinearLayout/android.widget.TextView').all():  # 获取视频分类列表
            top_bounds = self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/'
                                       'android.widget.FrameLayout[1]/android.widget.LinearLayout[1]//'
                                       'android.widget.LinearLayout[1]').get(timeout=3).bounds
        else:
            print('获取视频频道列表失败，请修改程序')
            raise
        for it, t in enumerate(video_pin_dao):
            t.click()
            time.sleep(1)
            for ci_shu in range(8):  # 向下滑动8次页面
                for isu, issue in enumerate(
                        self.pp.xpath(f'//android.widget.ListView/android.widget.FrameLayout').all()):
                    if down_bounds[1] > issue.bounds[1] > top_bounds[3]:
                        self.pp.click((issue.bounds[0] + issue.bounds[2]) / 2, issue.bounds[1])
                    elif down_bounds[1] > issue.bounds[3] > top_bounds[3]:
                        self.pp.click((issue.bounds[0] + issue.bounds[2]) / 2, issue.bounds[3])
                    else:
                        continue
                    self.pp(text='我的').wait_gone(timeout=5)
                    if self.pp(text='我的').exists:
                        continue
                    try:
                        title = self.pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                                              'android.view.View[1]/android.view.View[1]/android.view.View[1]/'
                                              'android.view.View[2]').get(timeout=10).text  # 获取标题
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
                    self.pp(text='继续播放').click_exists(timeout=1)
                    time.sleep(10)  # 每个视频学习10秒
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
                        # 点击积分,查一下积分完成情况
                        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/comm_head_xuexi_score"]').click(timeout=20)
                        job_temp = self.job_status()  # 查一下积分完成情况
                        need_video_num = int(job_temp[2][2]) - int(job_temp[2][1])
                        time.sleep(1)
                        if job_temp[2][0] == '已完成':  # 如果学习视频没完成，就开始学习
                            time.sleep(1)
                            self.pp(text='我的').click(timeout=20)
                            print('看视频任务已完成')
                            return
                time.sleep(1)
                self.pp(scrollable=True).scroll(steps=90)
                time.sleep(1)

    def look_tel(self, job_temp):  # 看电视台的视频，主要是用来弥补视频学习时长
        time.sleep(1)
        self.pp.press('back')  # 从我的界面回到app首页
        time.sleep(1)
        # 点击首页下面的电视台按钮
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_contact"]').click(timeout=20)
        time.sleep(1)
        self.pp(text='看电视').click(timeout=20)
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
            self.pp(text='继续播放').click_exists()
            self.pp(text='点击播放').click_exists()
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
                self.pp(text='我的').click(timeout=20)
                print('看视频任务已完成')
                return

    def read_issue_time(self, job_temp):
        time.sleep(1)
        self.pp.press('back')  # 从我的界面回到app首页
        time.sleep(1)
        # 点击首页下面的中间学习按钮
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').click(timeout=20)
        self.pp.xpath('//android.widget.ListView/android.widget.FrameLayout[1]').click_exists()
        self.pp.xpath('//android.widget.ListView/android.widget.FrameLayout[2]').click_exists()
        self.pp.xpath('//android.widget.ListView/android.widget.FrameLayout[3]').click_exists()
        t = time.time()
        while True:
            if time.time() - t > 120 * (int(job_temp[3][2]) - int(job_temp[3][1])):
                break
            self.pp(scrollable=True).scroll.vert.forward(steps=random.randint(130, 150))
            time.sleep(1)
            self.pp(scrollable=True).scroll.vert.backward(steps=random.randint(110, 130))
            time.sleep(1)
        time.sleep(1)
        self.pp.press('back')  # 从我的界面回到app首页
        time.sleep(1)
        self.pp(text='我的').click(timeout=20)

    def listen_tai_start(self):  # 听电台的音频开始程序，主要是用来弥补视频学习时长
        time.sleep(1)
        self.pp.press('back')  # 从我的界面回到app首页
        time.sleep(1)
        # 点击首页下面的电台按钮
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_mine"]').click(timeout=20)
        time.sleep(1)
        self.pp(text='听新闻广播').click(timeout=20)
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
        self.pp(text='我的').click(timeout=20)
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
        try:  # 点击电台按钮，打开电台控制栏
            self.pp.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                          'android.widget.FrameLayout[1]/android.widget.ImageView[1]').click(timeout=3)
        except uiautomator2.exceptions.XPathElementNotFoundError:
            self.pp.xpath('//android.widget.FrameLayout[3]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                          'android.widget.FrameLayout[1]/android.widget.ImageView[1]').click(timeout=3)
        except Exception as e:
            print('就没有打开收听电台的小栏目，只能重新看了', e)
            return False
        # 点击关闭按钮
        try:
            self.pp.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                          'android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                          'android.widget.ImageView[4]').click(timeout=1)
        except uiautomator2.exceptions.XPathElementNotFoundError:
            self.pp.xpath('//android.widget.FrameLayout[3]/android.widget.FrameLayout[1]/'
                          'android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                          'android.widget.ImageView[4]').click(timeout=1)
        self.pp.xpath('//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                      'android.widget.FrameLayout[1]/android.widget.ImageView[4]').wait_gone()
        self.pp.xpath('//android.widget.FrameLayout[3]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/'
                      'android.widget.FrameLayout[1]/android.widget.ImageView[4]').wait_gone()
        self.pp(text='我的').click_exists()
        time.sleep(1)
        return True

    def do_ding_yue(self):
        time.sleep(1)
        self.pp(text='订阅').click(timeout=20)
        self.pp(text='添加').click(timeout=20)
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
            self.pp(description="订阅").click_exists()
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
                self.pp(text='学习积分').click(timeout=20)
                job_stat = self.job_status()
            else:
                break

    def ben_di(self):
        time.sleep(1)
        while True:
            self.pp.press("back")
            time.sleep(1)
            if self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').exists:
                break
            time.sleep(1)
        # 点击首页下面的学习按钮
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/home_bottom_tab_button_work"]').click_exists()
        time.sleep(1)
        # 点击第四个标签栏，一般是北京频道
        self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/view_pager"]/android.widget.FrameLayout['
                      '1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]//android.widget.LinearLayout[4]'
                      ).click(timeout=20)
        # 点击第一个学习平台，北京学习平台
        self.pp.xpath('//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]').wait(timeout=10)
        self.pp.xpath('//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]').click_exists()
        print('已完成本地频道')
        time.sleep(1)
        self.pp.press('back')
        if self.pp.app_current()['package'] != 'cn.xuexi.android':
            self.pp.app_start('cn.xuexi.android')
        time.sleep(1)
        self.pp(text='我的').click(timeout=20)
        time.sleep(1)

    def job_status(self):
        time.sleep(1)
        self.pp(text='登录').wait(timeout=20)
        if not self.pp(text='登录').exists:
            print('网络有问题，请确保联网后重试')
            raise
        job_status1 = []
        for j in range(1, 15):
            while not self.pp.xpath(f'//android.widget.ListView/android.view.View[{j}]/android.view.View[4]').exists:
                self.pp(scrollable=True).scroll(steps=100)
                time.sleep(1)
            com = self.pp.xpath(f'//android.widget.ListView/android.view.View[{j}]/android.view.View[3]').get_text()
            com1, com2 = re.search(r'已获(\d*)分/每日上限(\d*)分', com).groups()
            sta = self.pp.xpath(f'//android.widget.ListView/android.view.View[{j}]/android.view.View[4]').get_text()
            title = self.pp.xpath(f'//android.widget.ListView/android.view.View[{j}]/android.view.View[1]/'
                                  f'android.view.View').get_text()
            job_status1.append((sta, com1, com2, title))
        self.pp.press('back')  # 查一下积分完成情况
        time.sleep(1)
        print('****************************************************')
        for k in job_status1:
            if k[0] != '已完成':
                print(f'{k[3]}  还没有完成，需要{k[2]}积分，只完成了{k[1]}积分')
        print('****************************************************')
        # print(job_status1)
        return job_status1

    def get_learn_num(self):
        time.sleep(1)
        self.pp(description='我的信息').click(timeout=20)
        time.sleep(1)
        self.learn_num = self.pp.xpath('//*[@resource-id="cn.xuexi.android:id/user_info_fragment_container"]'
                                       '/android.widget.LinearLayout[3]/android.widget.LinearLayout[1]'
                                       '/android.widget.TextView[2]').get_text()
        print('这个手机学习强国的学号是', self.learn_num)
        self.pp.press('back')
        time.sleep(1)

    def main_do(self, test=False):  # 主运行程序
        # self.pp.screen_on()
        self.pp.unlock()
        if self.unlock_password and self.pp(text='输入密码').exists(timeout=3):
            for k in self.unlock_password:
                self.pp(description=k).click()
                time.sleep(0.1)
            self.pp(text='输入密码').wait_gone()
        if test:
            self.test_pro()
        if 'cn.xuexi.android' in self.pp.app_list_running():
            self.pp.app_stop('cn.xuexi.android')
        self.pp.app_start('cn.xuexi.android')
        # 这个不能删，等待控件出现后再消失
        self.pp(resourceId='cn.xuexi.android:id/tvv_video_render').wait()
        self.pp(resourceId='cn.xuexi.android:id/tvv_video_render').wait_gone()
        # 检测是否登陆，如果没有登录就进行登录
        if self.pp(text='我的').click_exists(timeout=5):
            self.pp(resourceId='cn.xuexi.android:id/my_setting').click_exists(timeout=3)
            self.pp(text='退出登录').click_exists(timeout=3)
            self.pp(text='确认').click_exists(timeout=3)
        self.pp(text='登录').wait()
        self.pp(resourceId='cn.xuexi.android:id/et_phone_input').set_text(self.username)
        time.sleep(1)
        self.pp(resourceId='cn.xuexi.android:id/et_pwd_login').set_text(self.password)
        self.pp.xpath('//*[@resource-id="com.huawei.secime:id/char_keyboard_hide_btn"]').click_exists(timeout=1)
        self.pp(text='登录').click(timeout=2)
        self.pp(text='登录').wait_gone(timeout=5)
        if self.pp(text='连接失败，请检查你的网络后重试!').exists:
            print('网络不好，请重新连接网络')
            raise
        self.pp(text='我的').click_exists(timeout=20)
        time.sleep(1)
        self.get_learn_num()
        self.pp(text='学习积分').click_exists(timeout=20)
        self.pp(text='积分规则').wait()
        job_stat = self.job_status()
        self.pp(text='我的').wait()
        if job_stat[2][0] != '已完成':
            self.read_video(job_stat)
        else:
            print('已完成视频观看')
        if job_stat[4][0] != '已完成':
            t1 = self.listen_tai_start()
        else:
            t1 = 0
            print('已完成视听时长学习')
        if job_stat[9][0] != '已完成':
            self.run_ding_yue(job_stat)
        else:
            print('已完成订阅')
        if job_stat[1][0] != '已完成':
            self.read_issue(job_stat)
        else:
            print('已完成文章阅读')
        if job_stat[5][0] != '已完成':
            self.run_everyday_ti()
        else:
            print('已完成每日答题任务')
        if job_stat[6][0] != '已完成':
            self.run_every_week_ti()
        else:
            print('已完成每周答题任务')
        if job_stat[8][0] != '已完成':
            self.run_challenge()
        else:
            print('已完成挑战答题')
        if job_stat[4][0] != '已完成' and t1:
            self.listen_tai_end(job_stat, t1)
        else:
            print('已完成视听时长学习')
        if job_stat[13][0] != '已完成':
            self.ben_di()
        else:
            print('已完成本地频道')
        self.pp(text='学习积分').click()
        job_stat = self.job_status()
        time.sleep(1)
        if job_stat[3][0] != '已完成':
            self.read_issue_time(job_stat)
        if job_stat[4][0] != '已完成':
            self.look_tel(job_stat)
        if job_stat[7][0] != '已完成':
            self.run_special_ti()
        else:
            print('已完成专项答题任务')
        self.pp(resourceId='cn.xuexi.android:id/my_setting').click_exists(timeout=3)
        self.pp(text='退出登录').click_exists(timeout=3)
        self.pp(text='确认').click_exists(timeout=3)
        self.pp(text='登录').wait(timeout=20)
        self.pp.app_stop('cn.xuexi.android')
        time.sleep(1)
        self.pp.press('home')

    def recycle_main_do(self, cl_screen=False):
        t = time.time()
        while True:
            try:
                self.main_do()
                break
            except Exception as e:
                self.pp.screenshot(f'error-{e}-{random.random()}.jpg')
                if time.time() - t > 3600:
                    print('程序存在错误，试了一个小时都不行，请修改程序')
                    self.pp.app_stop('cn.xuexi.android')
                    break
                print(e)
                pass
        if cl_screen == 1:
            self.pp.screen_off()
        self.__del__()

    def test_pro(self):  # 测试专用程序
        print('开始测试程序了')
        # self.run_every_week_ti(test=True)
        # self.run_special_ti(test=True)
        while True:
            self.ben_di()
        # print(self.pp.dump_hierarchy())
        # self.run_everyday_ti()
        # self.run_challenge(ti_num=9999)
        # self.listen_tai_start()
        # job = [('已完成', '1', '1', '登录'), ('已完成', '0', '6', '阅读文章'), ('已完成', '6', '6', '视听学习'),
        #        ('已完成', '6', '6', '文章学习时长'), ('已完成', '6', '6', '视听学习时长'),
        #        ('已完成', '6', '6', '每日答题'), ('去答题', '0', '5', '每周答题'), ('去看看', '0', '10', '专项答题'),
        #        ('已完成', '6', '6', '挑战答题'), ('已完成', '2', '2', '订阅'), ('已完成', '1', '1', '收藏'),
        #        ('已完成', '1', '1', '分享'), ('已完成', '2', '2', '发表观点'), ('已完成', '1', '1', '本地频道')]
        # self.read_issue(job)
        raise


if __name__ == '__main__':
    DownTiKu().down_ti()
    # 要在对象创建时传入参数tesseract_path，表示pytesseract.pytesseract.tesseract_cmd的路径，
    # 否则使用默认值r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    phone_unlock_password = '850611'
    user_list = [
        # ['18810810611', 'jiajia0611'],
        ['18611001824', 'nopass.123'],
    ]
    for index_u, user in enumerate(user_list):
        do = QiangGuoFuZhu(username=user[0], password=user[1], unlock_password=phone_unlock_password)
        # do.main_do()
        # do.main_do(test=True)
        if index_u == len(user_list) - 1:
            do.recycle_main_do(cl_screen=True)
        else:
            do.recycle_main_do(cl_screen=False)
