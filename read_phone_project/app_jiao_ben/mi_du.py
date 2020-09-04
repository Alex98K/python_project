from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class MiDu(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(MiDu, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when(xpath='//*[@resource-id="com.lechuan.mdwz:id/t"]').click()
        # self.pp.watcher('tip5').when(xpath='//*[@resource-id="com.cashtoutiao:id/iv_close"]').click()
        # self.pp.watcher('tip6').when(xpath='//*[@resource-id="com.cashtoutiao:id/tt_video_ad_close_layout"]').click()
        self.pp.watcher.start(0.5)

    def sign_in(self):
        self.logger.info(f'开始签到')
        self.pp(text='福利').wait()
        self.pp(text='福利').click(offset=(random.random(), random.random()))
        if self.pp(description='去签到').exists(timeout=5):
            self.pp(description='去签到').click(offset=(random.random(), random.random()))

    def read_issue(self, duration, target_coin):
        self.logger.info(f'开始阅读文章')
        time.sleep(random.random() + 1)
        self.pp.xpath('//*[@resource-id="com.lechuan.mdwz:id/b3"]').wait()
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.lechuan.mdwz:id/b3"]').get().bounds)
        books = self.pp.xpath('//*[@resource-id="com.lechuan.mdwz:id/mb"]//android.view.ViewGroup/'
                              'android.widget.TextView[1]').all()
        if len(books) > 0:
            for i in books:
                self.click_random_position(i.bounds)
                self.pp.xpath('//*[@resource-id="com.lechuan.mdwz:id/a58"]').wait()
                t = time.time()
                while time.time() - t < duration:
                    self.scroll_read_novel()
                self.pp.press('back')
                time.sleep(random.random() + 1)
                return
        else:
            self.click_random_position(self.pp.xpath('//*[@resource-id="com.lechuan.mdwz:id/b1"]').get().bounds)
            time.sleep(random.random() + 1)
            self.click_random_position(self.pp.xpath(f'//*[@resource-id="com.lechuan.mdwz:id/a_k"]/'
                                                     f'android.widget.FrameLayout[2]').get().bounds)
            # 随机下滑2-4次
            for k in range(random.randint(2, 4)):
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                time.sleep(random.random())
            for j in self.pp.xpath('//*[@text="完结"]').all():
                self.click_random_position(self.pp.xpath(j.get_xpath() + '/../..').get().bounds)
                if self.pp(resourceId='com.lechuan.mdwz:id/um').exists(timeout=3):
                    self.pp.xpath('//*[@resource-id="com.lechuan.mdwz:id/a58"]').wait()
                    t = time.time()
                    while time.time() - t < duration:
                        self.scroll_read_novel()
                    self.pp.press('back')
                    time.sleep(random.random() + 1)
                    self.pp.press('back')
                    time.sleep(random.random() + 1)
                    return

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        t = time.time()
        while time.time() - t <= 60:
            if not self.pp(text="设置").exists:
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                time.sleep(random.random())
            else:
                break
        self.pp(text="设置").click(offset=(random.random(), random.random()))
        self.pp(text="清理缓存").wait()
        self.pp(text="清理缓存").click(offset=(random.random(), random.random()))
        time.sleep(random.random())

    def today_coin(self):
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(resourceId='com.lechuan.mdwz:id/atp').wait()
        time.sleep(random.random() + 1)
        coin = self.pp(resourceId='com.lechuan.mdwz:id/atp').get_text()
        read_time = self.pp(resourceId='com.lechuan.mdwz:id/au0').get_text().replace('今日阅读 ', '').replace('分钟', '')
        return int(coin), int(read_time)*60

    def main_do(self, duration, target_coin, cash_out):
        # self.scroll_read_novel()
        # raise
        self.app_start('米读极速版')
        # 过了开头的广告动画
        time.sleep(random.random() + 5)
        self.pp.xpath('//*[@resource-id="com.lechuan.mdwz:id/km"]').wait()
        self.pp.xpath('//*[@resource-id="com.lechuan.mdwz:id/km"]').wait_gone()
        print('123')
        self.pp(text='我的').wait(timeout=10)
        print('ad')
        if self.pp.xpath('//*[@resource-id="com.lechuan.mdwz:id/a58"]').exists:
            self.pp.press('back')
            self.pp(text='我的').wait(timeout=30)
            time.sleep(random.random() + 1)
        self.sign_in()
        coin, read_time = self.today_coin()
        if coin < target_coin and read_time < duration:
            self.read_issue(duration, target_coin)
        elif read_time >= duration:
            self.logger.info(f'今日已经获取超过{read_time}秒，不再阅读了')
        else:
            self.logger.info(f'今日已经获取超过{coin}个金币，不再阅读了')
        self.clean_cache()
        self.app_end()
