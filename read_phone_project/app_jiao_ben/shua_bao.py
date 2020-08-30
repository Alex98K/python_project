from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class ShuaBao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(ShuaBao, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        # self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip1').when('恭喜获得').press('back')
        self.pp.watcher('tip2').when(xpath='//*[@content-desc="送你金元宝 快来看我吧"]').call(self.watcher_call_1)
        self.pp.watcher.start(0.5)

    def watcher_call_1(self):
        self.pp.click(0.89, 0.209)

    def log_on(self):
        # 刷宝的只能通过短信登录
        self.logger.info(f'开始登录')
        self.pp(text='我').click(offset=(random.random(), random.random()))

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
        # self.pp(description='当前余额').wait()
        # coin = self.pp.xpath('//*[@content-desc="我的元宝"]/following-sibling::android.view.View') \
        #     .get().attrib['content-desc'].replace(',', '')
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

    def _read_issue_core(self, time1, time2):
        read_issue_time = random.randint(time1, time2)  # 看视频总时间
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
            self.pp.swipe(random.uniform(0.3, 0.7), random.uniform(0.7, 0.8), random.uniform(0.3, 0.7),
                          random.uniform(0, 0.2), steps=random.randint(20, 60))

    def read_issue_first(self):
        self.logger.info(f'开始阅读首页视频')
        time.sleep(random.random() + 1)
        self.pp.xpath('//*[@resource-id="com.jm.video:id/tabLayout"]/android.widget.LinearLayout[1]/'
                      'android.widget.RelativeLayout[1]').wait()
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.jm.video:id/tabLayout"]/'
                                                 'android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]')
                                   .get().bounds)
        time.sleep(random.random() + 1)
        self._read_issue_core(900, 1200)

    def read_issue_city(self):
        # 直播不得金币，暂时不看
        self.logger.info(f'开始阅读直播视频')
        time.sleep(random.random() + 1)
        self.pp.xpath('//*[@resource-id="com.jm.video:id/tabLayout"]/android.widget.LinearLayout[1]/'
                      'android.widget.RelativeLayout[2]').wait()
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.jm.video:id/tabLayout"]/'
                                                 'android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]')
                                   .get().bounds)
        self.pp(description='直播').wait()
        time.sleep(random.random() + 1)
        for j in range(random.randint(0, 5)):  # 随机下滑几次
            self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                          random.uniform(0.2, 0.3), steps=random.randint(20, 60))
        temp_bounds = self.pp.xpath(f'//*[@content-desc="刷宝短视频"]/android.view.View[{random.randint(9, 20)}]').bounds
        self.click_random_position(temp_bounds)  # 随机选页面中的视频
        self._read_issue_core(600, 900)

    def read_issue(self):
        read_issue_time = random.randint(3000, 4000)  # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time and self.today_coin() <= 10000:
            self.read_issue_first()
            # if self.today_coin() > 10000:
            #     break
            # self.read_issue_city()

    def main_do(self):
        # raise
        self.app_start('刷宝')
        self.pp(text='我').wait(timeout=30)
        # self.log_on()
        self.sign_in()
        self.read_issue()
        self.clean_cache()
        self.app_end()
