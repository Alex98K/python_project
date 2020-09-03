from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class JinDong(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(JinDong, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip2').when('残忍离开').click()
        self.pp.watcher.start(0.5)

    def read_issue_first(self, time1, time2):
        self.logger.info(f'开始阅读首页视频')
        time.sleep(random.random() + 1)
        self.pp(description='我的').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self._read_adv(time1, time2)

    def _read_adv(self, time1, time2):
        for j in self.pp.xpath('//*[@resource-id="com.jd.jdlite.lib.personal:id/card_business_container"]/'
                               'android.support.v7.widget.RecyclerView[1]//android.widget.RelativeLayout').all():
            title = self.pp.xpath(j.get_xpath() + '/android.widget.TextView[1]').get_text()
            bounds = self.pp.xpath(j.get_xpath() + '/android.widget.Button').get().bounds
            self.click_random_position(bounds)
            time.sleep(random.random() + 1)
            if title in ['逛商品赚金币', '逛活动赚金币']:
                t = time.time()
                while time.time() - t < random.uniform(time1, time2):
                    self.scroll_read_issue()
                    time.sleep(random.random() + 1)
                    if self.pp(resourceId='com.jd.jdlite:id/ll_task_bottom_next').exists:
                        self.pp(resourceId='com.jd.jdlite:id/ll_task_bottom_next')\
                            .click(offset=(random.random(), random.random()))
                        time.sleep(random.random() + 1)
            elif title == '看视频赚金币':
                xpath = self.pp.xpath(f'//android.support.v7.widget.RecyclerView/android.widget.FrameLayout[{random.randint(1, 4)}]')
                xpath.wait()
                self.click_random_position(xpath.get().bounds)
                time.sleep(random.uniform(time1, time2))
        t = time.time()
        while time.time() - t < 60 or not self.pp(description='我的').exists:
            time.sleep(1)
            self.pp.press('back')

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.pp(description='我的').wait()
        self.pp(description='我的').click(offset=(random.random(), random.random()))
        self.pp.xpath('//*[@resource-id="com.jd.jdlite.lib.personal:id/attention_view"]/'
                      'android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.TextView[1]').wait()
        coin = self.pp.xpath('//*[@resource-id="com.jd.jdlite.lib.personal:id/attention_view"]/'
                             'android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/'
                             'android.widget.TextView[1]').get_text().replace(' 个', '')
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
        self.app_start('京东极速版')
        self.pp(description='我的').wait(timeout=30)
        self.read_issue(duration, target_coin)
        self.clean_cache()
        self.app_end()
