from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class JinRiTouTiao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(JinRiTouTiao, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip2').when(xpath='//*[@resource-id="com.ss.android.article.lite:id/b6y"]').click()
        self.pp.watcher('tip3').when(xpath='//*[@resource-id="com.ss.android.article.lite:id/a0j"]').click()
        self.pp.watcher('tip4').when(xpath='//*[@text="0x+wcp2R1bM4bU8gAAAABJRU5ErkJggg=="]').click()
        self.pp.watcher.start(0.5)

    def sign_in(self):
        self.logger.info(f'开始签到')
        self.pp(text='任务').wait()
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 5)
        if self.pp.xpath('//android.app.Dialog/android.view.View[1]/android.view.View[2]/android.view.View[5]').exists:
            self.click_random_position(self.pp.xpath('//android.app.Dialog/android.view.View[1]/android.view.View[2]/'
                                                     'android.view.View[5]').get().bounds)

    def _adjust_lan_mu(self):
        self.logger.info(f'开始调整栏目')
        lan_mu_num_end = len(self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/a4x"]/'
                                           'android.widget.LinearLayout[1]//android.widget.FrameLayout').all()) - 1
        if lan_mu_num_end <= 5:
            return
        if self.pp(resourceId="com.ss.android.article.lite:id/a9k").exists:
            self.pp(resourceId="com.ss.android.article.lite:id/a9k").click(
                offset=(random.uniform(0.5, 0.9), random.random()))
            time.sleep(random.random() + 1)
            self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/a2f"]/android.view.View[3]').wait()
            self.pp.click(0.928, 0.107)
            time.sleep(random.random() + 1)
        lan_mu_num = 2
        for j in reversed(self.pp(resourceId='com.ss.android.article.lite:id/a9q')):
            j.click_exists()
        time.sleep(random.random() + 1)
        for j in reversed(self.pp(resourceId='com.ss.android.article.lite:id/au5')):
            if j.get_text()[-2:] not in ['抗疫', '视频', '图片', '值点', '小说', '音频', '娱乐'] and \
                    random.random() < 0.5 and lan_mu_num < lan_mu_num_end:
                j.click_exists()
                lan_mu_num += 1
        time.sleep(random.random() + 1)
        self.pp.click(0.928, 0.107)
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def read_issue(self, duration, target_coin):
        self.logger.info(f'开始阅读文章')
        time.sleep(random.random() + 1)
        self.click_random_position(self.pp.xpath('//*[@resource-id="android:id/tabs"]/android.widget.RelativeLayout[1]')
                                   .get().bounds)
        time.sleep(random.random() + 1)
        # 看情况调整栏目
        if self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/a4x"]/android.widget.LinearLayout[1]/'
                         'android.widget.FrameLayout[last()]').get().bounds[2] > \
                self.pp(resourceId="com.ss.android.article.lite:id/a9k").bounds()[0]:
            self._adjust_lan_mu()
        # 获取栏目
        lan_mu_num = len(self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/a4x"]/'
                                       'android.widget.LinearLayout[1]//android.widget.FrameLayout').all())
        random_list = [x for x in range(1, lan_mu_num)]
        random.shuffle(random_list)
        for j in random_list:
            t = time.time()
            self.click_random_position(self.pp.xpath(f'//*[@resource-id="com.ss.android.article.lite:id/a4x"]/'
                                                     f'android.widget.LinearLayout[1]//'
                                                     f'android.widget.FrameLayout[{j + 1}]').get().bounds)
            time.sleep(random.random() + 1)
            for i in range(random.randint(8, 12)):  # 每个栏目下滑随机次
                # 每个栏目下的文章标题
                for title in self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/'
                                           'bz" or @resource-id="com.ss.android.article.lite:id/km"]').all():
                    # 需要满足看文章概率
                    if random.random() >= self.probability_read_issue:
                        continue
                    self.click_random_position(title.bounds)
                    time.sleep(random.random() + 2)
                    # 如果是搜索按钮点进去的，那就跳过
                    if self.pp(description='返回').exists:
                        self.pp.press('back')
                        time.sleep(random.random() + 1)
                    # 没有奖励的就跳过不看了
                    if not (self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/aak"]').exists or
                            self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/l9"]').exists) or \
                            self.pp.xpath('//*[@resource-id="com.ss.android.newugc:id/round_write_button"]').exists or\
                            self.pp.xpath('//*[@resource-id="com.ss.android.newugc:id/'
                                          'wenda_detail_title_image"]').exists:
                        self.pp.press('back')
                        time.sleep(random.random() + 1)
                        continue
                    issue_time_start = time.time()  # 开始计时
                    read_issue_time = random.randrange(5, 125)  # 看文章的随机时间
                    read_video_time = random.randrange(5, 185)  # 看视频的随机时间
                    # 按照设定的关注概率，随机关注
                    if self.pp(text="关注").exists and random.random() < self.probability_focus:
                        self.pp(text="关注").click(offset=(random.random(), random.random()))
                        time.sleep(random.random() + 1)
                    # 看下是视频还是文章，视频就停着看，文章就下滑看
                    if not self.pp.xpath('//*[@resource-id="header"]').exists:
                        while not (self.pp(text='重播').exists or time.time() - issue_time_start > read_video_time):
                            if self.pp(text='关闭广告').exists:
                                self.pp(text='关闭广告').click(offset=(random.random(), random.random()))
                            time.sleep(1)
                    else:
                        while time.time() - issue_time_start <= read_issue_time:
                            time.sleep(random.uniform(3, 5))
                            self.scroll_read_issue()
                        self.pp(scrollable=True).scroll.toEnd(steps=10)
                    # 按照设定的点赞概率，随机点赞
                    if self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/b2w"]/'
                                     'android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/'
                                     'android.widget.ImageView[2]').exists and \
                            random.random() < self.probability_thumb_up:
                        self.click_random_position(self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/'
                                                                 'b2w"]/android.widget.LinearLayout[1]/'
                                                                 'android.widget.LinearLayout[1]/'
                                                                 'android.widget.ImageView[2]').get().bounds)
                        time.sleep(random.random() + 1)
                    # 按照设定的评论概率，随机评论
                    if self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/yu"]').exists and \
                            random.random() < self.probability_commit:
                        self.click_random_position(self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/'
                                                                 'yu"]').get().bounds)
                        time.sleep(random.random() + 1)
                        self.pp(resourceId='com.ss.android.article.lite:id/b5g').wait()
                        self.pp(resourceId='com.ss.android.article.lite:id/b5g') \
                            .set_text(random.choice(self.commit))
                        time.sleep(random.random() + 1)
                        self.pp(text='发布').click(offset=(random.random(), random.random()))
                        time.sleep(random.random() + 1)
                    # 阅读完看一下今日金币数量，有可能卡住，先不用了
                    # if self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/aak"]').exists:
                    #     self.click_random_position(self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/'
                    #                                              'aak"]').get().bounds)
                    #     self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/a0p"]').wait()
                    #     coin = self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/a0p"]').get_text()
                    #     self.pp.press('back')
                    #     time.sleep(random.random() + 1)
                    #     if int(coin) > target_coin:
                    #         self.logger.info(f'已经阅读获得了 {coin} 金币')
                    #         self.pp.press('back')
                    #         time.sleep(random.random() + 1)
                    #         return
                    #     else:
                    #         self.pp.press('back')
                    #         time.sleep(random.random() + 1)
                    # 阅读完文章返回
                    while not self.pp(text='我的').exists:
                        self.pp.press('back')
                        time.sleep(random.random() + 1)
                    time.sleep(random.random() + 1)
                    if time.time() - t > duration:
                        self.logger.info(f'今日阅读时间超过了{duration}秒，不再阅读了')
                        return
                # 随机下滑1-4次
                for k in range(random.randint(1, 4)):
                    self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                  random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                    time.sleep(random.random())
            time.sleep(random.random() + 1)
            coin_len = self.today_coin()
            if coin_len < target_coin:
                self.click_random_position(self.pp.xpath('//*[@resource-id="android:id/tabs"]/'
                                                         'android.widget.RelativeLayout[1]').get().bounds)
                time.sleep(random.random() + 1)
            else:
                self.logger.info(f'今日已经获取超过 {target_coin} 个金币，不再阅读了')
                return
            self.logger.info('看完这个栏目了，换个栏目')

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/ya"]').wait()
        coin = self.pp.xpath('//*[@resource-id="com.ss.android.article.lite:id/ya"]').get_text()
        time.sleep(random.random() + 1)
        if 'w' in coin:
            coin = int(float(coin.replace('w', '')) * 10000)
        else:
            coin = int(coin)
        self.logger.info(f'今日已经获取金币 {coin}')
        return coin

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(text="系统设置").wait()
        self.pp(text="系统设置").click(offset=(random.random(), random.random()))
        self.pp(text="清除缓存").wait()
        self.pp(text="清除缓存").click(offset=(random.random(), random.random()))
        self.pp(text="确认").wait()
        self.pp(text="确认").click(offset=(random.random(), random.random()))

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('今日头条极速版')
        self.pp(text='我的').wait(timeout=30)
        self.sign_in()
        coin = self.today_coin()
        if coin < target_coin:
            self.read_issue(duration, target_coin)
        self.clean_cache()
        self.app_end()
