from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class XiaoTangGao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(XiaoTangGao, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip2').when('暂不领取').click()
        self.pp.watcher('tip3').when(xpath='//*[@resource-id="com.jifen.ponycamera:id/rl_close"]').click()
        self.pp.watcher.start(0.5)

    def _read_issue_core(self, read_issue_time):
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            time.sleep(random.uniform(3, 10))
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('//*[@resource-id="com.jifen.ponycamera:id/tv_like"]').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.ponycamera:id/tv_like"]')
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
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.ponycamera:id/main_bottom_layout"]/'
                                                 'android.widget.FrameLayout[5]').get().bounds)
        self.pp.xpath('//*[@content-desc="今日金币"]').wait()
        time.sleep(random.random() + 2)
        coin = self.pp.xpath('//*[@content-desc="今日金币"]/preceding-sibling::android.view.View[1]') \
            .get().attrib['content-desc'].replace(',', '')
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

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('小糖糕')
        self.pp(text='我的').wait(timeout=30)
        self.read_issue(duration, target_coin)
        self.app_end()
