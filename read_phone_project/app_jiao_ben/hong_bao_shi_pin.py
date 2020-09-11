from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class HongBaoShiPin(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(HongBaoShiPin, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip3').when('取消').click()
        self.pp.watcher('tip2').when(xpath='//*[@resource-id="com.sanmiao.sound:id/iv_signIn_close"]').click()
        self.pp.watcher.start(0.5)

    def sign_in(self):
        self.logger.info(f'开始签到')
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        if self.pp(text='立即签到').exists(timeout=3):
            self.pp(text='立即签到').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)

    def _read_issue_core(self, read_issue_time):
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            time.sleep(random.uniform(15, 25))
            self.scroll_read_issue()

    def read_issue_first(self, read_issue_time):
        self.logger.info(f'开始阅读首页视频')
        time.sleep(random.random() + 1)
        self.pp(text='首页').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self._read_issue_core(read_issue_time)

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.pp(text='我').wait()
        self.pp(text='我').click(offset=(random.random(), random.random()))
        self.pp.xpath('//*[@resource-id="com.sanmiao.sound:id/tv_mine_gold"]').wait()
        coin = self.pp.xpath('//*[@resource-id="com.sanmiao.sound:id/tv_mine_gold"]') \
            .get_text()
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

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('红包视频')
        self.pp(text='我').wait(timeout=30)
        self.sign_in()
        self.read_issue(duration, target_coin)
        self.app_end()
