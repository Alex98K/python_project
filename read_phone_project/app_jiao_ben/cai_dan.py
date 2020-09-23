from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time
import re


class CaiDan(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(CaiDan, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip2').when(xpath='//*[@content-desc="加载中"]/android.view.View[1]/android.view.View[2]/'
                                           'android.view.View[2]').click()
        self.pp.watcher('tip3').when(xpath='//*[@resource-id="com.jifen.dandan:id/close_bottom_button"]').click()
        self.pp.watcher('tip5').when(xpath='//*[@resource-id="com.jifen.dandan:id/tv_upgrade_cancel"]').click()
        self.pp.watcher('tip4').when(xpath='//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/'
                                           'android.widget.RelativeLayout[1]/android.widget.ImageView[1]').click()
        self.pp.watcher.start(0.5)

    def _read_issue_core(self, read_issue_time):
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            # 如果不小心切换到了关注栏目，就回到推荐栏目
            if self.pp(text='音乐').exists:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.dandan:id/title_container"]/'
                                                         'android.widget.FrameLayout[3]/android.widget.TextView[1]')
                                           .get().bounds)
            # time.sleep(random.uniform(3, 5))
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('com.jifen.dandan:id/iv_like_icon').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('com.jifen.dandan:id/iv_like_icon').get().bounds)
                time.sleep(random.random() + 1)
            # 按照设定的关注概率，随机关注
            if self.pp.xpath('//*[@resource-id="com.jifen.dandan:id/fl_follow_view"]').exists and \
                    random.random() < self.probability_focus:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.dandan:id/fl_follow_view"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
            # 按照设定的评论概率，随机评论
            if self.pp.xpath('com.jifen.dandan:id/iv_comment_icon').exists and \
                    random.random() < self.probability_commit:
                self.click_random_position(self.pp.xpath('com.jifen.dandan:id/iv_comment_icon').get().bounds)
                time.sleep(random.random() + 1)
                if self.pp(resourceId='com.jifen.dandan:id/text_add_comment').exists:
                    self.pp(resourceId='com.jifen.dandan:id/text_add_comment') \
                        .click(offset=(random.random(), random.random()))
                self.pp(resourceId='com.jifen.dandan:id/et_input').wait()
                self.pp(resourceId='com.jifen.dandan:id/et_input').set_text(random.choice(self.commit))
                time.sleep(random.random() + 1)
                self.pp(resourceId='com.jifen.dandan:id/tv_send').click(offset=(random.random(), random.random()))
                time.sleep(random.random() + 1)
                self.pp.press('back')
                time.sleep(random.random() + 1)
            if self.pp(description='我的金币').exists:
                self.pp.press('back')
            self.scroll_read_issue()

    def read_issue_first(self, read_issue_time):
        self.logger.info(f'开始阅读首页视频')
        time.sleep(random.random() + 1)
        self.pp(text='首页').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp(resourceId='com.jifen.dandan:id/lottie_view_gold') \
            .drag_to(resourceId='com.jifen.dandan:id/iv_ugc_enter', duration=random.uniform(0.25, 0.5))
        time.sleep(random.random() + 1)
        self._read_issue_core(read_issue_time)

    def read_issue_city(self, read_issue_time):
        self.logger.info(f'开始阅读发现视频')
        self.pp(text='发现').click(offset=(random.random(), random.random()))
        self.pp(resourceId='com.jifen.dandan:id/title_container').wait()
        self.pp(resourceId='com.jifen.dandan:id/title_container').child()[random.randint(2, 4)] \
            .click(offset=(random.random(), random.random()))
        for j in range(random.randint(0, 2)):  # 随机下滑几次
            self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                          random.uniform(0.2, 0.3), steps=random.randint(20, 60))
        time.sleep(random.random() + 1)
        temp_bounds = self.pp.xpath(f'//*[@resource-id="com.jifen.dandan:id/taskcenter_rv"]/'
                                    f'android.widget.LinearLayout[{random.randint(1, 4)}]/'
                                    f'android.view.ViewGroup[1]').bounds
        self.click_random_position(temp_bounds)  # 随机选页面中的视频
        time.sleep(random.random() + 1)
        self._read_issue_core(read_issue_time)
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.pp(text='我').wait()
        self.pp(text='我').click(offset=(random.random(), random.random()))
        # time.sleep(random.random() + 2)
        self.pp(resourceId='com.jifen.dandan:id/tv_person_today_gold_title').wait()
        self.pp.swipe(random.uniform(0.25, 0.7), random.uniform(0.15, 0.25), random.uniform(0.25, 0.7),
                      random.uniform(0.65, 0.8), steps=random.randint(20, 60))
        time.sleep(random.random() + 2)
        self.pp(resourceId='com.jifen.dandan:id/tv_person_today_gold_title').wait()
        coin = self.pp(resourceId='com.jifen.dandan:id/tv_person_today_gold_title').get_text().replace(',', '')
        coin = re.search(r'\d*', coin).group()
        if 'w' in coin:
            coin = int(float(coin.replace('w', '')) * 10000)
        else:
            coin = int(coin)
        self.logger.info(f'今日已经获取金币 {coin}')
        return coin

    def read_issue(self, duration, target_coin):
        # 看视频总时间
        read_issue_time1, read_issue_time2 = random.randint(600, 900), random.randint(300, 600)
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= duration and self.today_coin() <= target_coin:
            self.read_issue_first(read_issue_time1)
            # if self.today_coin() > target_coin:
            #     break
            # self.read_issue_city(read_issue_time2)

    def cash_out(self, cash_out):
        super(CaiDan, self).cash_out(cash_out)
        self.pp(text='我').wait()
        self.pp(text='我').click(offset=(random.random(), random.random()))
        self.pp(resourceId='com.jifen.dandan:id/tv_person_total_gold_title').wait()
        self.pp(resourceId='com.jifen.dandan:id/tv_person_total_gold_title')\
            .click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 3)
        coin = self.pp.xpath('//*[@resource-id="com.jifen.dandan:id/content_view"]/android.widget.RelativeLayout[1]/'
                             'android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[3]/'
                             'android.view.View[1]/android.view.View').get_text()
        coin = int(coin)
        if coin > 300000:
            self.pp(description='30').click(offset=(random.random(), random.random()))
            self.pp(description='立即提现').wait()
            self.pp(description='立即提现').click(offset=(random.random(), random.random()))

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('彩蛋视频')
        self.pp(text='我').wait(timeout=30)
        self.read_issue(duration, target_coin)
        if cash_out:
            self.cash_out(cash_out)
        self.app_end()
