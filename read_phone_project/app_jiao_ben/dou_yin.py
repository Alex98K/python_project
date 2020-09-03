from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class DouYin(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(DouYin, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip2').when('残忍离开').click()
        self.pp.watcher.start(0.5)

    def sign_in(self):
        self.logger.info(f'开始签到')
        self.pp(resourceId='com.ss.android.ugc.aweme.lite:id/az8').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 5)
        if self.pp(text='签到').count > 1:
            self.pp(text='签到')[1].click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def _read_issue_core(self, time1, time2):
        read_issue_time = random.randint(time1, time2)  # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            # 如果不小心切换到了关注栏目，就回到推荐栏目
            if self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/ax_"]').get().center()[0]\
                    < self.pp(text='关注').bounds()[2]:
                self.pp(text='推荐').click(offset=(random.random(), random.random()))
            time.sleep(random.uniform(3, 10))
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/ww"]').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/ww"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
            # 按照设定的关注概率，随机关注
            if self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/d14"]').exists and \
                    random.random() < self.probability_focus:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/d14"]')
                                           .get().bounds)
                if self.pp(text='关注').exists(timeout=3):
                    self.pp(text='关注').click(offset=(random.random(), random.random()))
                time.sleep(random.random() + 3)
                self.pp.press('back')
                time.sleep(random.random() + 1)
            # 按照设定的评论概率，随机评论
            if self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/qb"]').exists and \
                    random.random() < self.probability_commit:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/qb"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
                if self.pp(text='留下你的精彩评论吧').exists:
                    self.pp(text='留下你的精彩评论吧').click(offset=(random.random(), random.random()))
                self.pp(text='留下你的精彩评论吧').wait()
                self.pp(text='留下你的精彩评论吧').set_text(random.choice(self.commit))
                time.sleep(random.random() + 1)
                self.pp(resourceId='com.ss.android.ugc.aweme.lite:id/qp') \
                    .click(offset=(random.random(), random.random()))
                time.sleep(random.random() + 1)
                self.pp.press('back')
                time.sleep(random.random() + 1)
            self.scroll_read_issue()

    def read_issue_first(self, time1, time2):
        self.logger.info(f'开始阅读首页视频')
        time.sleep(random.random() + 1)
        self.pp(text='首页').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self._read_issue_core(time1, time2)

    def read_issue_city(self, time1, time2):
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
        self._read_issue_core(time1, time2)

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.pp(resourceId='com.ss.android.ugc.aweme.lite:id/azz').wait()
        self.pp(resourceId='com.ss.android.ugc.aweme.lite:id/azz').click(offset=(random.random(), random.random()))
        self.pp.xpath('//*[@content-desc="Luckycat"]/android.view.View[2]').wait()
        coin = self.pp.xpath('//*[@content-desc="Luckycat"]/android.view.View[2]') \
            .get().attrib['content-desc'].replace(',', '')
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
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= duration and self.today_coin() <= target_coin:
            self.read_issue_first(600, 900)
            if self.today_coin() > target_coin:
                break
            self.read_issue_city(300, 600)

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我').click(offset=(random.random(), random.random()))
        self.pp(description='更多').wait()
        self.pp(description='更多').click(offset=(random.random(), random.random()))
        self.pp(text="设置").wait()
        self.pp(text="设置").click(offset=(random.random(), random.random()))
        t = time.time()
        while time.time() - t < 60:
            if not self.pp(text="清理缓存").exists:
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                time.sleep(random.random())
            else:
                break
        self.pp(text="清理缓存").wait()
        self.pp(text="清理缓存").click(offset=(random.random(), random.random()))
        self.pp(text="清理").wait()
        self.pp(text="清理").click(offset=(random.random(), random.random()))

    def main_do(self, duration, target_coin):
        # raise
        self.app_start('抖音极速版')
        self.pp(text='我').wait(timeout=30)
        self.sign_in()
        self.read_issue(duration, target_coin)
        self.clean_cache()
        self.app_end()
