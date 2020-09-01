from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class TianTianAiQingLi(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(TianTianAiQingLi, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip2').when('暂不领取').click()
        self.pp.watcher('tip3').when(xpath='//*[@resource-id="com.xiaoqiao.qclean:id/rl_close"]').click()
        self.pp.watcher.start(0.5)

    def log_on(self):
        self.logger.info(f'开始登录')
        self.pp(text='我').click(offset=(random.random(), random.random()))
        if self.pp(text='密码登录').exists(timeout=5):
            self.pp(text='密码登录').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
            self.pp(resourceId="com.ss.android.ugc.aweme.lite:id/b9k").clear_text()
            self.pp(resourceId="com.ss.android.ugc.aweme.lite:id/b9k").click(offset=(random.random(), random.random()))
            self.input_num('15611895793')
            time.sleep(random.random() + 1)
            self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/b8p"]').set_text('jiajia0611')
            time.sleep(random.random() + 1)
            self.pp(text='登录').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
        else:
            return

    def sign_in(self):
        self.logger.info(f'开始签到')
        self.pp(text='任务').wait()
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp(text='我的金币').wait()
        time.sleep(random.random() + 5)

    def _read_issue_core(self, time1, time2):
        read_issue_time = random.randint(time1, time2)  # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            # 如果不小心切换到了关注栏目，就回到推荐栏目
            # if self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/ax_"]').get().center()[0]\
            #         < self.pp(text='关注').bounds()[2]:
            #     self.pp(text='推荐').click(offset=(random.random(), random.random()))
            time.sleep(random.uniform(3, 10))
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('com.xiaoqiao.qclean:id/tv_like').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('com.xiaoqiao.qclean:id/tv_like').get().bounds)
                time.sleep(random.random() + 1)
            # 按照设定的关注概率，随机关注
            # if self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/d14"]').exists and \
            #         random.random() < self.probability_focus:
            #     self.click_random_position(self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/d14"]')
            #                                .get().bounds)
            #     if self.pp(text='关注').exists(timeout=3):
            #         self.pp(text='关注').click(offset=(random.random(), random.random()))
            #     time.sleep(random.random() + 3)
            #     self.pp.press('back')
            #     time.sleep(random.random() + 1)
            # 按照设定的评论概率，随机评论
            if self.pp.xpath('//*[@resource-id="com.xiaoqiao.qclean:id/feed_video_comment"]').exists and \
                    random.random() < self.probability_commit:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.xiaoqiao.qclean:id/feed_video_comment"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
                if self.pp(resourceId='com.xiaoqiao.qclean:id/feed_comment_reply').exists:
                    self.pp(resourceId='com.xiaoqiao.qclean:id/feed_comment_reply').click(offset=(random.random(), random.random()))
                self.pp(resourceId='com.xiaoqiao.qclean:id/acomment_edt_comment').wait()
                self.pp(resourceId='com.xiaoqiao.qclean:id/acomment_edt_comment').set_text(random.choice(self.commit))
                time.sleep(random.random() + 1)
                self.pp(resourceId='com.xiaoqiao.qclean:id/acomment_btn_send')\
                    .click(offset=(random.random(), random.random()))
                time.sleep(random.random() + 1)
                self.pp.press('back')
                time.sleep(random.random() + 1)
            self.scroll_read_issue()

    def read_issue_first(self):
        self.logger.info(f'开始阅读视频')
        time.sleep(random.random() + 1)
        self.pp(text='视频').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self._read_issue_core(900, 1200)

    def read_issue_city(self):
        self.logger.info(f'开始阅读同城视频')
        self.pp(text='同城').click(offset=(random.random(), random.random()))
        for j in range(random.randint(0, 5)):  # 随机下滑几次
            self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                          random.uniform(0.2, 0.3), steps=random.randint(20, 60))
        time.sleep(random.random() + 1)
        temp_bounds = self.pp.xpath(f'//*[@resource-id="com.ss.android.ugc.aweme.lite:id/as7"]/'
                                    f'android.view.ViewGroup[{random.randint(1, 4)}]/'
                                    f'android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/'
                                    f'android.widget.RelativeLayout[1]/android.view.View[1]').bounds
        self.click_random_position(temp_bounds)  # 随机选页面中的视频
        time.sleep(random.random() + 1)
        self._read_issue_core(600, 900)

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.pp(text='我的').wait()
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp.xpath('//*[@text="金币余额"]/preceding-sibling::android.view.View[1]').wait()
        time.sleep(random.random() + 5)
        coin = self.pp.xpath('//*[@text="金币余额"]/preceding-sibling::android.view.View[1]') \
            .get_text().replace(',', '')
        time.sleep(random.random() + 1)
        if 'w' in coin:
            coin = int(float(coin.replace('w', '')) * 10000)
        else:
            coin = int(coin)
        self.logger.info(f'今日已经获取金币 {coin}')
        return coin

    def read_issue(self):
        read_issue_time = random.randint(3000, 4000)  # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time and self.today_coin() <= 5000:
            self.read_issue_first()
            # if self.today_coin() > 10000:
            #     break
            # self.read_issue_city()

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(description='我的钱包').wait()
        self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                      random.uniform(0.2, 0.3), steps=random.randint(10, 20))
        time.sleep(random.random() + 1)
        self.pp.click(0.87, 0.87)
        self.pp(text='清除缓存').wait()
        self.pp(text='清除缓存').click(offset=(random.random(), random.random()))

    def main_do(self):
        # print(self.pp.dump_hierarchy())
        # raise
        self.app_start('天天爱清理')
        self.pp(text='我的').wait(timeout=30)
        # self.log_on()
        self.sign_in()
        self.read_issue()
        self.clean_cache()
        self.app_end()
