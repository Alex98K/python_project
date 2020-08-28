from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class DouYin(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(DouYin, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        # self.pp.watcher('tip2').when('残忍离开').click()
        self.pp.watcher.start(0.5)

    def log_on(self):
        self.logger.info(f'开始登录')
        self.pp(text='我').click(offset=(random.random(), random.random()))
        if self.pp(text='密码登录').exists(timeout=5):
            self.pp(text='密码登录').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
            self.pp(resourceId="com.ss.android.ugc.aweme.lite:id/b9k").clear_text()
            self.pp(resourceId="com.ss.android.ugc.aweme.lite:id/b9k").click(offset=(random.random(), random.random()))
            self.input_num('15611895793')
            time.sleep(random.random() + 1)
            self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/b8p"]').set_text('jiajia0611')
            time.sleep(random.random() + 1)
            self.pp(text='登录').click(offset=(random.random(), random.random()))
        else:
            # read_time = self.pp.xpath('//*[@resource-id="com.jifen.qukan.personal:id/ee"]').get_text()
            return

    def sign_in(self):
        self.logger.info(f'开始签到')
        self.pp(resourceId='com.ss.android.ugc.aweme.lite:id/azz').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 5)
        if self.pp(text='签到').count > 1:
            self.pp(text='签到')[1].click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def read_issue(self):
        self.logger.info(f'开始阅读文章')
        self.pp(text='首页').click(offset=(random.random(), random.random()))
        read_issue_time = random.randint(3000, 4000)  # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while True:
            time.sleep(random.uniform(5, 10))
            self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                          random.uniform(0.2, 0.3), random.uniform(0.1, 0.3))
            time.sleep(1)
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/ww"]').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/ww"]')
                                           .get().bounds)
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
                self.pp(resourceId='com.ss.android.ugc.aweme.lite:id/qp')\
                    .click(offset=(random.random(), random.random()))
                time.sleep(random.random() + 1)
                self.pp.press('back')
                time.sleep(random.random() + 1)
            if time.time() - issue_time_start > read_issue_time:
                break

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我').click(offset=(random.random(), random.random()))
        self.pp(description='更多').wait()
        self.pp(description='更多').click(offset=(random.random(), random.random()))
        self.pp(text="设置").wait()
        self.pp(text="设置").click(offset=(random.random(), random.random()))
        while True:
            if not self.pp(text="清理缓存").exists:
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), random.uniform(0.1, 0.3))
                time.sleep(random.random())
            else:
                break
        self.pp(text="清理缓存").wait()
        self.pp(text="清理缓存").click(offset=(random.random(), random.random()))
        self.pp(text="清理").wait()
        self.pp(text="清理").click(offset=(random.random(), random.random()))

    def main_do(self):
        # raise
        self.app_start('抖音极速版')
        self.pp(text='我').wait(timeout=30)
        self.log_on()
        self.sign_in()
        self.read_issue()
        self.clean_cache()
        # self.coin_info()
        self.app_end()
