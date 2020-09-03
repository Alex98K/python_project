from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class CaiDan(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(CaiDan, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip2').when(xpath='//*[@content-desc="加载中"]/android.view.View[1]/android.view.View[2]/'
                                           'android.view.View[2]').click()
        self.pp.watcher('tip3').when(xpath='//*[@resource-id="com.jifen.dandan:id/close_bottom_button"]').click()
        self.pp.watcher.start(0.5)

    def _read_issue_core(self, time1, time2):
        read_issue_time = random.randint(time1, time2)  # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            # 如果不小心切换到了关注栏目，就回到推荐栏目
            if self.pp(text='音乐').exists:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.dandan:id/title_container"]/'
                                                         'android.widget.FrameLayout[3]/android.widget.TextView[1]')
                                           .get().bounds)
            time.sleep(random.uniform(3, 10))
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
                    self.pp(resourceId='com.jifen.dandan:id/text_add_comment')\
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

    def read_issue_first(self, time1, time2):
        self.logger.info(f'开始阅读首页视频')
        time.sleep(random.random() + 1)
        self.pp(text='首页').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp(resourceId='com.jifen.dandan:id/lottie_view_gold')\
            .drag_to(resourceId='com.jifen.dandan:id/iv_ugc_enter', duration=random.uniform(0.25, 0.5))
        time.sleep(random.random() + 1)
        self._read_issue_core(time1, time2)

    def read_issue_city(self, time1, time2):
        self.logger.info(f'开始阅读发现视频')
        self.pp(text='发现').click(offset=(random.random(), random.random()))
        self.pp(resourceId='com.jifen.dandan:id/title_container').wait()
        self.pp(resourceId='com.jifen.dandan:id/title_container').child()[random.randint(2, 4)]\
            .click(offset=(random.random(), random.random()))
        for j in range(random.randint(0, 5)):  # 随机下滑几次
            self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                          random.uniform(0.2, 0.3), steps=random.randint(20, 60))
        time.sleep(random.random() + 1)
        temp_bounds = self.pp.xpath(f'//*[@resource-id="com.jifen.dandan:id/taskcenter_rv"]/'
                                    f'android.widget.LinearLayout[{random.randint(1, 4)}]/'
                                    f'android.view.ViewGroup[1]').bounds
        self.click_random_position(temp_bounds)  # 随机选页面中的视频
        time.sleep(random.random() + 1)
        self._read_issue_core(time1, time2)
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.pp(resourceId='com.jifen.dandan:id/fl_welfare_task').wait()
        self.pp(resourceId='com.jifen.dandan:id/fl_welfare_task').click(offset=(random.random(), random.random()))
        self.pp.xpath('//*[@content-desc="加载中..."]').wait_gone()
        self.pp.xpath('//*[@resource-id="coins-number"]').wait()
        time.sleep(random.random() + 2)
        coin = self.pp.xpath('//*[@resource-id="coins-number"]').get().attrib['content-desc'].replace(',', '')
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)
        if 'w' in coin:
            coin = int(float(coin.replace('w', '')) * 10000)
        else:
            coin = int(coin)
        self.logger.info(f'今日已经获取金币 {coin}')
        return coin

    def read_issue(self, duration, target_coin):
        # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= duration and self.today_coin() <= target_coin:
            self.read_issue_first(600, 900)
            if self.today_coin() > target_coin:
                break
            self.read_issue_city(300, 600)

    def main_do(self, duration, target_coin):
        # raise
        self.app_start('彩蛋视频')
        self.pp(text='我').wait(timeout=30)
        self.read_issue(duration, target_coin)
        self.app_end()
