from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class HuiTouTiao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(HuiTouTiao, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip4').when(xpath='//*[@resource-id="com.cashtoutiao:id/img_close"]').click()
        self.pp.watcher('tip5').when(xpath='//*[@resource-id="com.cashtoutiao:id/iv_close"]').click()
        self.pp.watcher('tip6').when(xpath='//*[@resource-id="com.cashtoutiao:id/tt_video_ad_close_layout"]').click()
        self.pp.watcher.start(0.5)

    def sign_in(self):
        self.logger.info(f'开始签到')
        if self.pp(text='签到').exists(timeout=5):
            self.pp(text='签到').click(offset=(random.random(), random.random()))

    def _adjust_lan_mu(self):
        self.logger.info(f'开始调整栏目')
        lan_mu_num_end = len(self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/tab_news"]/'
                                           'android.widget.LinearLayout[1]//android.widget.FrameLayout/'
                                           'android.widget.RelativeLayout[1]').all()) - 1
        if lan_mu_num_end <= 5:
            return
        if self.pp(resourceId="com.cashtoutiao:id/iv_edit").exists:
            self.pp(resourceId="com.cashtoutiao:id/iv_edit").click(offset=(random.uniform(0.5, 0.9), random.random()))
            time.sleep(random.random() + 1)
        lan_mu_num = 0
        for j in reversed(self.pp(resourceId='com.cashtoutiao:id/text_channel')):
            if j.get_text() not in ['三农', '故事', '国外', '星座', '教育', '旅行', '游戏', '关注', '文化', '时尚', '体育', '图片'] or \
                    random.random() < 0.3 or lan_mu_num >= lan_mu_num_end:
                j.sibling(resourceId='com.cashtoutiao:id/app_delete_btn').click_exists()
            else:
                lan_mu_num += 1
        self.pp(text='完成').wait()
        self.pp(text='完成').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def read_issue(self):
        self.logger.info(f'开始阅读文章')
        time.sleep(random.random() + 1)
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/tabs"]/'
                                                 'android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/'
                                                 'android.widget.FrameLayout[1]/android.widget.LinearLayout[1]')
                                   .get().bounds)
        time.sleep(random.random() + 1)
        # 看情况调整栏目
        if self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/tab_news"]/android.widget.LinearLayout[1]//'
                         'android.widget.FrameLayout[last()]').get().bounds[2] > \
                self.pp(resourceId="com.cashtoutiao:id/iv_edit").bounds()[0]:
            self._adjust_lan_mu()
        # 获取栏目
        lan_mu_num = len(self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/tab_news"]/'
                                       'android.widget.LinearLayout[1]//android.widget.FrameLayout/'
                                       'android.widget.RelativeLayout[1]').all())
        random_list = [x for x in range(lan_mu_num)]
        random.shuffle(random_list)
        for j in random_list:
            self.click_random_position(self.pp.xpath(f'//*[@resource-id="com.cashtoutiao:id/tab_news"]/'
                                                     f'android.widget.LinearLayout[1]/android.widget.FrameLayout[{j+1}]'
                                                     f'/android.widget.RelativeLayout[1]').get().bounds)
            time.sleep(random.random() + 1)
            for i in range(random.randint(8, 12)):  # 每个栏目下滑随机次
                # 每个栏目下的文章标题
                for title in self.pp.xpath('com.cashtoutiao:id/tv_title').all():
                    # 需要满足看文章概率
                    if random.random() >= self.probability_read_issue:
                        continue
                    self.click_random_position(title.bounds)
                    time.sleep(random.random() + 2)
                    # 如果有获取金币的图标，才看，没有就返回,
                    if self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/news_income_container"]').exists:
                        issue_time_start = time.time()  # 开始计时
                        read_issue_time = random.randrange(5, 125, 30)  # 看文章的随机时间
                        read_video_time = random.randrange(5, 185, 30)  # 看视频的随机时间
                        # 按照设定的关注概率，随机关注
                        if self.pp(description="关注").exists and random.random() < self.probability_focus:
                            self.pp(description="关注").click(offset=(random.random(), random.random()))
                            time.sleep(random.random() + 1)
                        # 看下是视频还是文章，视频就停着看，文章就下滑看
                        if self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/video_container"]').exists:
                            while not (self.pp(text='重播').exists or time.time() - issue_time_start > read_video_time):
                                if self.pp(text='关闭广告').exists:
                                    self.pp(text='关闭广告').click(offset=(random.random(), random.random()))
                                time.sleep(1)
                        else:
                            while time.time() - issue_time_start <= read_issue_time:
                                time.sleep(random.uniform(3, 5))
                                self.scroll_read_issue()
                                if self.pp.xpath('//*[@content-desc="展开全文"]').exists:
                                    self.click_random_position(self.pp.xpath('//*[@content-desc="展开全文"]').get().bounds)
                                # if not self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/g3"]').exists:
                                #     self.pp.press('back')
                        # 按照设定的点赞概率，随机点赞
                        if self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/iv_collection"]').exists and \
                                random.random() < self.probability_thumb_up:
                            self.click_random_position(self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/'
                                                                     'iv_collection"]').get().bounds)
                            time.sleep(random.random() + 1)
                        # 按照设定的评论概率，随机评论
                        if self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/rl_comment"]').exists and \
                                random.random() < self.probability_commit:
                            self.click_random_position(self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/'
                                                                     'rl_comment"]').get().bounds)
                            time.sleep(random.random() + 1)
                            self.pp(resourceId='com.cashtoutiao:id/up_keyboard').wait()
                            self.pp(resourceId='com.cashtoutiao:id/up_keyboard') \
                                .click(offset=(random.random(), random.random()))
                            self.pp(resourceId='com.cashtoutiao:id/comment_editText').wait()
                            self.pp(resourceId='com.cashtoutiao:id/comment_editText') \
                                .set_text(random.choice(self.commit))
                            time.sleep(random.random() + 1)
                            self.pp(text='发布').click(offset=(random.random(), random.random()))
                            time.sleep(random.random() + 1)
                    time.sleep(random.random() + 1)
                    self.pp.press('back')
                    time.sleep(random.random() + 1)
                if not self.pp(text='我的').exists:
                    self.pp.press('back')
                    time.sleep(random.random() + 1)
                # 随机下滑2-4次
                for k in range(random.randint(2, 4)):
                    self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                  random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                    time.sleep(random.random())
            time.sleep(random.random() + 1)
            coin_len = self.today_coin()
            if coin_len < 6:
                self.logger.info(f'已经阅读获得了{coin_len}位数金币')
                self.click_random_position(self.pp.xpath(
                    '//*[@resource-id="com.cashtoutiao:id/tabs"]/android.widget.LinearLayout[1]/'
                    'android.widget.FrameLayout[1]').get().bounds)
                time.sleep(random.random() + 1)
            else:
                self.logger.info(f' 惠头条 今日已经获取超过10000个金币，不再阅读了')
                return
            self.logger.info('看完这个栏目了，换个栏目')

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        t = time.time()
        while time.time() - t <= 60:
            if not self.pp(text="系统设置").exists:
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                time.sleep(random.random())
            else:
                break
        self.pp(text="系统设置").click(offset=(random.random(), random.random()))
        self.pp(text="清除缓存").wait()
        self.pp(text="清除缓存").click(offset=(random.random(), random.random()))
        time.sleep(random.random())
        self.pp(text="清除中...").wait_gone()

    def today_coin(self):
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(text='今日收益(金币)').wait()
        return len(self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/setting_today_gold"]//'
                                 'android.view.View').all())

    def main_do(self):
        # raise
        self.app_start('惠头条')
        # 过了开头的广告动画
        self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/iv_animate_logo"]').wait()
        self.pp.xpath('//*[@resource-id="com.cashtoutiao:id/iv_animate_logo"]').wait_gone()
        self.pp(text='我的').wait(timeout=30)
        self.sign_in()
        coin_len = self.today_coin()
        if coin_len < 6:
            self.read_issue()
        else:
            self.logger.info(f' 惠头条 今日已经获取超过10000个金币，不再阅读了')
        self.clean_cache()
        self.app_end()
