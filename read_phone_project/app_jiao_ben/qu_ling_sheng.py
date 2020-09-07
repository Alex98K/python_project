from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class QuLingSheng(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(QuLingSheng, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip2').when('暂不领取').click()
        self.pp.watcher('tip3').when(xpath='//*[@resource-id="com.zheyun.bumblebee:id/iv_close"]').click()
        self.pp.watcher('tip4').when(xpath='//*[@resource-id="com.zheyun.bumblebee:id/base_card_dialog_close"]').click()
        self.pp.watcher.start(0.5)

    def sign_in(self):
        self.logger.info(f'开始签到')
        self.pp(text='任务').wait()
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 5)

    def _read_issue_core(self, read_issue_time):
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            # 如果不小心切换到了关注栏目，就回到推荐栏目
            if self.pp(text='小剧场').exists:
                self.pp(text='推荐').click(offset=(random.random(), random.random()))
            time.sleep(random.uniform(3, 10))
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('//*[@resource-id="com.zheyun.bumblebee:id/tv_like"]').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.zheyun.bumblebee:id/tv_like"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
            self.scroll_read_issue()

    def read_issue_first(self, read_issue_time):
        self.logger.info(f'开始阅读小视频')
        time.sleep(random.random() + 1)
        self.pp(text='小视频').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self._read_issue_core(read_issue_time)

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.pp(text='我的').wait()
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp.xpath('//*[@content-desc="今日金币"]').wait()
        time.sleep(random.random() + 2)
        coin = self.pp.xpath('//*[@text="今日金币"]/preceding-sibling::android.view.View[1]') \
            .get_text().replace(',', '')
        time.sleep(random.random() + 1)
        if 'w' in coin:
            coin = int(float(coin.replace('w', '')) * 10000)
        else:
            coin = int(coin)
        self.logger.info(f'今日已经获取金币 {coin}')
        return coin

    def read_issue(self, duration, target_coin):
        read_issue_time = random.randint(300, 600)
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= duration and self.today_coin() <= target_coin:
            self.read_issue_first(read_issue_time)

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        t = time.time()
        while time.time() - t < 60:
            if not self.pp(text="设置").exists or self.pp(text="设置").bounds()[3] > \
                    self.pp(resourceId='com.zheyun.bumblebee:id/amain_view_bottom').bounds()[1]:
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                time.sleep(random.random())
            else:
                break
        t = time.time()
        while time.time() - t < 60:
            self.pp(text="设置").wait()
            self.pp(text="设置").click(offset=(random.random(), random.random()))
            if self.pp(text="我的钱包").exists(timeout=3):
                self.pp.press('back')
            else:
                break
            time.sleep(random.random() + 1)
        self.pp(text="清除缓存").wait()
        self.pp(text="清除缓存").click(offset=(random.random(), random.random()))

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('趣铃声')
        self.pp(text='我的').wait(timeout=30)
        self.sign_in()
        self.read_issue(duration, target_coin)
        self.clean_cache()
        self.app_end()
