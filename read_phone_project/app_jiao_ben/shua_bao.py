from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class ShuaBao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(ShuaBao, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip1').when('恭喜获得').press('back')
        self.pp.watcher('tip2').when(xpath='//*[@content-desc="送你金元宝 快来看我吧"]').call(self.watcher_call_1)
        self.pp.watcher.start(0.5)

    def watcher_call_1(self):
        self.pp.click(0.89, 0.209)

    def sign_in(self):
        self.logger.info(f'开始签到')
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.jm.video:id/tabLayout"]/'
                                                 'android.widget.LinearLayout[1]/android.widget.RelativeLayout[4]')
                                   .get().bounds)
        self.pp(description='当前余额').wait()
        if self.pp(description='立即签到').exists(timeout=3):
            self.pp(description='立即签到').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
        time.sleep(random.random() + 1)

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.jm.video:id/tabLayout"]/'
                                                 'android.widget.LinearLayout[1]/android.widget.RelativeLayout[5]')
                                   .get().bounds)
        time.sleep(random.random() + 1)
        coin = self.pp.xpath('//*[@resource-id="com.jm.video:id/tv_gold_num"]').get_text()
        time.sleep(random.random() + 1)
        if 'w' in coin:
            coin = int(float(coin.replace('w', '')) * 10000)
        else:
            coin = int(coin)
        self.logger.info(f'今日已经获取金币 {coin}')
        return coin

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我').click(offset=(random.random(), random.random()))
        self.pp(resourceId='com.jm.video:id/iv_setting').click(offset=(random.random(), random.random()))
        self.pp(text='清理缓存').wait()
        self.pp(text='清理缓存').click(offset=(random.random(), random.random()))

    def _read_issue_core(self, read_issue_time):
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            # 如果不小心切换到了关注栏目，就回到推荐栏目
            if self.pp(resourceId='com.jm.video:id/iv_live_head').exists:
                self.pp(text='推荐').click(offset=(random.random(), random.random()))
            time.sleep(random.uniform(3, 10))
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('//*[@resource-id="com.jm.video:id/image_view"]').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.jm.video:id/image_view"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
            # 按照设定的关注概率，随机关注
            if self.pp(text='+ 关注').exists(timeout=3) and random.random() < self.probability_focus:
                self.pp(text='+ 关注').click(offset=(random.random(), random.random()))
                time.sleep(random.random() + 3)
            # 按照设定的评论概率，随机评论
            if self.pp.xpath('//*[@resource-id="com.jm.video:id/comment"]').exists and \
                    random.random() < self.probability_commit:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.jm.video:id/comment"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
                if not self.pp(text='暂不支持评论').exists:
                    self.pp(resourceId='com.jm.video:id/editComment').wait()
                    self.pp(resourceId='com.jm.video:id/editComment').click(offset=(random.random(), random.random()))
                    self.pp(resourceId='com.jm.video:id/et_comment').wait()
                    self.pp.set_fastinput_ime(False)
                    self.pp(resourceId='com.jm.video:id/et_comment').set_text(random.choice(self.commit))
                    time.sleep(random.random() + 1)
                    self.pp.click(0.909, 0.95)
                    time.sleep(random.random() + 1)
                self.pp.press('back')
                time.sleep(random.random() + 1)
            self.scroll_read_issue()

    def read_issue_first(self, read_issue_time):
        self.logger.info(f'开始阅读首页视频')
        time.sleep(random.random() + 1)
        self.pp.xpath('//*[@resource-id="com.jm.video:id/tabLayout"]/android.widget.LinearLayout[1]/'
                      'android.widget.RelativeLayout[1]').wait()
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.jm.video:id/tabLayout"]/'
                                                 'android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]')
                                   .get().bounds)
        time.sleep(random.random() + 1)
        self._read_issue_core(read_issue_time)

    def read_issue(self, duration, target_coin):
        read_issue_time = random.randint(300, 600)
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= duration and self.today_coin() <= target_coin:
            self.read_issue_first(read_issue_time)

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('刷宝')
        self.pp(text='我').wait(timeout=30)
        self.sign_in()
        self.read_issue(duration, target_coin)
        self.clean_cache()
        self.app_end()
