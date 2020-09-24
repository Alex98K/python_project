from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class HuoShan(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(HuoShan, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher.start(0.5)

    def _read_issue_core(self, read_issue_time):
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            # time.sleep(random.uniform(3, 5))
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('//*[@resource-id="com.ss.android.ugc.livelite:id/p9"]').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.ss.android.ugc.livelite:id/p9"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
            # 按照设定的关注概率，随机关注
            if self.pp.xpath('com.ss.android.ugc.livelite:id/po').exists and \
                    random.random() < self.probability_focus:
                self.click_random_position(self.pp.xpath('com.ss.android.ugc.livelite:id/po').get().bounds)
                time.sleep(random.random() + 1)
            # 按照设定的评论概率，随机评论
            if self.pp.xpath('//*[@resource-id="com.ss.android.ugc.livelite:id/p5"]').exists and \
                    random.random() < self.probability_commit:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.ss.android.ugc.livelite:id/p5"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
                if self.pp(resourceId='com.ss.android.ugc.livelite:id/lk').exists:
                    self.pp(resourceId='com.ss.android.ugc.livelite:id/lk')\
                        .click(offset=(random.random(), random.random()))
                self.pp(resourceId='com.ss.android.ugc.livelite:id/lk').wait()
                self.pp(resourceId='com.ss.android.ugc.livelite:id/lk').set_text(random.choice(self.commit))
                time.sleep(random.random() + 1)
                self.pp(resourceId='com.ss.android.ugc.livelite:id/ln').click(offset=(random.random(), random.random()))
                time.sleep(random.random() + 1)
                self.pp.press('back')
                time.sleep(random.random() + 1)
                self.pp.press('back')
                time.sleep(random.random() + 1)
            self.scroll_read_issue()

    def read_issue_first(self, read_issue_time):
        self.logger.info(f'开始阅读首页视频')
        time.sleep(random.random() + 1)
        self.pp(text='首页').wait()
        self.pp(text='首页').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self._read_issue_core(read_issue_time)

    def read_issue_city(self, read_issue_time):
        self.logger.info(f'开始阅读推荐视频')
        self.pp(text='推荐').click(offset=(random.random(), random.random()))
        for j in range(random.randint(0, 2)):  # 随机下滑几次
            self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                          random.uniform(0.2, 0.3), steps=random.randint(20, 60))
        time.sleep(random.random() + 1)
        t2 = time.time()
        while time.time() - t2 < 60 and not self.pp\
                .xpath('//*[@resource-id="com.ss.android.ugc.livelite:id/ss"]').exists:
            temp_bounds = self.pp.xpath(f'//*[@resource-id="com.ss.android.ugc.livelite:id/w8"]/'
                                        f'android.widget.RelativeLayout[{random.randint(1, 2)}]').get().bounds
            self.click_random_position(temp_bounds)  # 随机选页面中的视频
            time.sleep(random.random() + 2)
        if time.time() - t2 > 50:
            time.sleep(random.random() + 1)
            self.pp.press('back')
            time.sleep(random.random() + 1)
            return
        self._read_issue_core(read_issue_time)
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(resourceId='com.ss.android.ugc.livelite:id/lu').wait()
        time.sleep(random.random() + 1)
        coin = self.pp(resourceId='com.ss.android.ugc.livelite:id/lu').get_text()
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
        read_issue_time1, read_issue_time2 = random.randint(600, 900), random.randint(300, 600)
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= duration and self.today_coin() <= target_coin:
            self.read_issue_first(read_issue_time1)
            if self.today_coin() > target_coin:
                break
            self.read_issue_city(read_issue_time2)

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        t = time.time()
        while time.time() - t <= 60:
            if not self.pp(text="设置").exists or self.pp(text="设置").bounds()[3] \
                    > self.pp(resourceId="com.ss.android.ugc.livelite:id/xc").bounds()[1]:
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                time.sleep(1)
            else:
                break
        self.pp(text="设置").wait()
        self.pp(text="设置").click(offset=(random.random(), random.random()))
        self.pp(text="清理缓存").wait()
        self.pp(text="清理缓存").click(offset=(random.random(), random.random()))
        self.pp(text="确定").wait()
        self.pp(text="确定").click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 3)

    def sig_in(self):
        self.logger.info('开始签到')
        self.pp(text='红包').wait()
        self.pp(text='红包').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 5)

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('火山极速版')
        self.pp(text='我的').wait(timeout=30)
        self.sig_in()
        self.read_issue(duration, target_coin)
        self.clean_cache()
        self.app_end()
