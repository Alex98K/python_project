from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class SouHuZiXun(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(SouHuZiXun, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when(xpath='//*[@resource-id="com.sohu.infonews:id/cancle_dialog_iv"]').click()
        self.pp.watcher('tip2').when(xpath='//*[@resource-id="com.sohu.infonews:id/act_close_image"]').click()
        # self.pp.watcher('tip5').when(xpath='//*[@resource-id="com.cashtoutiao:id/iv_close"]]').click()
        # self.pp.watcher('tip6').when(xpath='//*[@resource-id="com.cashtoutiao:id/tt_video_ad_close_layout"]').click()
        self.pp.watcher.start(0.5)

    def sign_in(self):
        self.logger.info(f'开始签到')
        self.pp(text='任务').wait()
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        if self.pp(text='签到').exists(timeout=5):
            self.pp(text='签到').click(offset=(random.random(), random.random()))
            if self.pp(text='我笑纳了').exists(timeout=5):
                self.pp(text='我笑纳了').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
            self.pp.press('back')
            time.sleep(random.random() + 1)

    def _adjust_lan_mu(self):
        self.logger.info(f'开始调整栏目')
        lan_mu_num_end = len(self.pp.xpath('//*[@resource-id="com.sohu.infonews:id/tab_bar"]/'
                                           'android.widget.LinearLayout[1]//android.widget.RelativeLayout').all()) - 1
        if lan_mu_num_end <= 5:
            return
        self.pp(resourceId="com.sohu.infonews:id/channel_more").wait()
        self.pp(resourceId="com.sohu.infonews:id/channel_more") \
            .click(offset=(random.uniform(0.5, 0.9), random.random()))
        time.sleep(random.random() + 1)
        self.pp(resourceId="com.sohu.infonews:id/textview_recyclerview_add_item_one").wait()
        self.pp(resourceId="com.sohu.infonews:id/textview_recyclerview_add_item_one") \
            .click(offset=(random.uniform(0.5, 0.9), random.random()))
        time.sleep(random.random() + 1)
        for i in reversed(self.pp.xpath('//*[@resource-id="com.sohu.infonews:id/recylerView_channel"]//'
                                        'android.widget.FrameLayout/android.widget.ImageView[1]').all()):
            self.click_random_position(i.bounds)
            time.sleep(random.random() + 0.5)
        time.sleep(random.random() + 1)
        lan_mu_num = 1
        for j in reversed(self.pp(resourceId='com.sohu.infonews:id/textview_recyelerview_add_item_pindao')):
            if j.get_text() not in ['抗肺炎', '党媒推荐'] and \
                    random.random() < 0.2 and lan_mu_num <= lan_mu_num_end:
                j.click(offset=(random.random(), random.random()))
                lan_mu_num += 1
        self.pp(text='完成').wait()
        self.pp(text='完成').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def read_issue(self, duration, target_coin):
        self.logger.info(f'开始阅读文章')
        time.sleep(random.random() + 1)
        self.pp(text="首页").wait()
        self.pp(text="首页").click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        # 看情况调整栏目
        if self.pp.xpath('//*[@resource-id="com.sohu.infonews:id/tab_bar"]/android.widget.LinearLayout[1]/'
                         'android.widget.RelativeLayout[last()]').get().bounds[2] > \
                self.pp(resourceId="com.sohu.infonews:id/channel_more").bounds()[0]:
            self._adjust_lan_mu()
        # 获取栏目
        lan_mu_num = len(self.pp.xpath('//*[@resource-id="com.sohu.infonews:id/tab_bar"]/'
                                       'android.widget.LinearLayout[1]//android.widget.RelativeLayout').all())
        random_list = [x for x in range(lan_mu_num)]
        random.shuffle(random_list)
        t = time.time()
        for j in random_list:
            time.sleep(random.random() + 1)
            self.click_random_position(self.pp.xpath(f'//*[@resource-id="com.sohu.infonews:id/tab_bar"]/'
                                                     f'android.widget.LinearLayout[1]/android.widget.RelativeLayout'
                                                     f'[{j+1}]/android.widget.RelativeLayout[1]').get().bounds)
            time.sleep(random.random() + 1)
            for i in range(random.randint(8, 12)):  # 每个栏目下滑随机次
                # 每个栏目下的文章标题
                for title in self.pp.xpath('com.sohu.infonews:id/article_title').all():
                    # 需要满足看文章概率
                    if random.random() >= self.probability_read_issue:
                        continue
                    # 如果是广告，就跳过
                    if self.pp.xpath(title.get_xpath() + '/..//*[@resource-id="com.sohu.infonews:id/tv_ad_flag"]') \
                            .exists:
                        continue
                    self.click_random_position(title.bounds)
                    time.sleep(random.random() + 2)
                    # 如果有获取金币的图标，才看，没有就返回,
                    if not self.pp.xpath('//*[@resource-id="com.sohu.infonews:id/counting_img"]').exists:
                        time.sleep(random.random() + 1)
                        self.pp.press('back')
                        continue
                    # 如果跳转到其他app ，就回来
                    if (tp := self.pp.app_current()['package']) != self.package_name:
                        self.pp.app_stop(tp)
                        time.sleep(random.random() + 1)
                        self.pp.app_start(self.package_name)
                        continue
                    # 如果跳到了安装app的界面，就回来
                    if self.pp(text="取消").exists:
                        self.pp(text="取消").click(offset=(random.random(), random.random()))
                        time.sleep(random.random() + 1)
                        continue
                    issue_time_start = time.time()  # 开始计时
                    read_issue_time = random.randrange(5, 125)  # 看文章的随机时间
                    read_video_time = random.randrange(5, 185)  # 看视频的随机时间
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
                    # 按照设定的评论概率，随机评论
                    if self.pp.xpath('//*[@resource-id="com.sohu.infonews:id/add_comment"]').exists and \
                            random.random() < self.probability_commit:
                        self.click_random_position(self.pp.xpath('//*[@resource-id="com.sohu.infonews:id/'
                                                                 'add_comment"]').get().bounds)
                        time.sleep(random.random() + 1)
                        self.pp(resourceId='com.sohu.infonews:id/comment_input').wait()
                        self.pp(resourceId='com.sohu.infonews:id/comment_input') \
                            .set_text(random.choice(self.commit))
                        time.sleep(random.random() + 1)
                        self.pp(resourceId='com.sohu.infonews:id/comment_write_ok') \
                            .click(offset=(random.random(), random.random()))
                        time.sleep(random.random() + 1)
                    time.sleep(random.random() + 1)
                    self.pp.press('back')
                    time.sleep(random.random() + 1)
                    if time.time() - t > duration:
                        self.logger.info(f'今日阅读时间超过了{duration}秒，不再阅读了')
                        return
                self.app_switch_current()
                # 随机下滑1-4次
                for k in range(random.randint(1, 4)):
                    self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                  random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                    time.sleep(random.random())
            time.sleep(random.random() + 1)
            coin_len = self.today_coin()
            if coin_len < target_coin:
                self.logger.info(f'已经阅读获得了 {coin_len} 金币')
                self.click_random_position(self.pp.xpath(
                    '//*[@resource-id="com.sohu.infonews:id/footer_view"]/android.widget.RelativeLayout[1]/'
                    'android.widget.RelativeLayout[1]').get().bounds)
                time.sleep(random.random() + 1)
            else:
                self.logger.info(f'今日已经获取超过 {coin_len} 金币，不再阅读了')
                return
            self.logger.info('看完这个栏目了，换个栏目')

    def today_coin(self):
        self.pp(text='任务').wait()
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        self.pp.xpath('//*[@resource-id="com.sohu.infonews:id/money_item"]/android.widget.LinearLayout[1]/'
                      'android.widget.TextView[2]').wait()
        coin = self.pp.xpath('//*[@resource-id="com.sohu.infonews:id/money_item"]/android.widget.LinearLayout[1]/'
                             'android.widget.TextView[2]').get_text().replace(',', '')
        time.sleep(random.random() + 1)
        self.logger.info(f'已经获取 {coin} 金币')
        return int(coin)

    def cash_out(self, cash_out):
        if not cash_out:
            return
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(text='兑换提现').wait()
        self.pp(text='兑换提现').click(offset=(random.random(), random.random()))
        self.pp(text='提现方式').wait()
        time.sleep(random.random() + 1)
        coin = int(self.pp(resourceId='com.cashtoutiao:id/tv_tips_gold_coin').get_text()
                   .replace(' 金币', '').replace(',', ''))
        if coin >= 10000:
            self.pp(resourceId='com.cashtoutiao:id/rl_wechat').wait()
            self.pp(resourceId='com.cashtoutiao:id/rl_wechat').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
            self.pp(resourceId='com.cashtoutiao:id/item_view').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
            self.pp(resourceId='com.cashtoutiao:id/tv_withdraw').click(offset=(random.random(), random.random()))
        t = time.time()
        while not self.pp(text='我的').exists and time.time() - t < 60:
            self.pp.press('back')
            time.sleep(random.random() + 1)

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('搜狐资讯')
        self.pp(text='任务').wait(timeout=30)
        self.sign_in()
        if self.today_coin() < target_coin:
            self.read_issue(duration, target_coin)
        else:
            self.logger.info(f'今日已经获取超过目标金币，不再阅读了')
        self.cash_out(cash_out)
        self.app_end()
