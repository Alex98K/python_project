from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class WeiShi(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(WeiShi, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip2').when('知道了').click()
        self.pp.watcher.start(0.5)

    def _read_issue_core(self, time1, time2):
        read_issue_time = random.randint(time1, time2)  # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            # 如果不小心切换到了关注栏目，就回到推荐栏目
            if self.pp.xpath('//*[@resource-id="com.tencent.weishi:id/oyw"]').exists:
                self.pp(text='推荐').click(offset=(random.random(), random.random()))
            time.sleep(random.uniform(3, 10))
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('//*[@resource-id="com.tencent.weishi:id/ndw"]/android.view.ViewGroup[1]/'
                             'android.view.ViewGroup[2]/android.widget.FrameLayout[1]').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.tencent.weishi:id/ndw"]/android.view'
                                                         '.ViewGroup[1]/android.view.ViewGroup[2]/'
                                                         'android.widget.FrameLayout[1]').get().bounds)
                time.sleep(random.random() + 1)
            # 按照设定的关注概率，随机关注
            if self.pp.xpath('//*[@resource-id="com.tencent.weishi:id/ndw"]/android.view.ViewGroup[1]/'
                             'android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]/'
                             'android.widget.FrameLayout[1]').exists and random.random() < self.probability_focus:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.tencent.weishi:id/ndw"]/'
                                                         'android.view.ViewGroup[1]/android.view.ViewGroup[1]/'
                                                         'android.view.ViewGroup[1]/android.widget.LinearLayout[1]/'
                                                         'android.widget.FrameLayout[1]').get().bounds)
            # 按照设定的评论概率，随机评论
            if self.pp.xpath('//*[@resource-id="com.tencent.weishi:id/ndw"]/android.view.ViewGroup[1]/'
                             'android.view.ViewGroup[2]/android.widget.ImageView[1]').exists and \
                    random.random() < self.probability_commit:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.tencent.weishi:id/ndw"]/'
                                                         'android.view.ViewGroup[1]/android.view.ViewGroup[2]/'
                                                         'android.widget.ImageView[1]').get().bounds)
                time.sleep(random.random() + 1)
                self.pp(resourceId='com.tencent.weishi:id/qlp').wait()
                self.pp(resourceId='com.tencent.weishi:id/qlp').click(offset=(random.random(), random.random()))
                self.pp(resourceId='com.tencent.weishi:id/qlp').wait()
                self.pp(resourceId='com.tencent.weishi:id/qlp').set_text(random.choice(self.commit))
                time.sleep(random.random() + 1)
                self.pp(resourceId='com.tencent.weishi:id/kwc').click(offset=(random.random(), random.random()))
                time.sleep(random.random() + 1)
                self.pp.press('back')
                time.sleep(random.random() + 1)
            self.scroll_read_issue()

    def read_issue_first(self):
        self.logger.info(f'开始阅读首页视频')
        time.sleep(random.random() + 1)
        self.pp(resourceId='com.tencent.weishi:id/qff').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self._read_issue_core(900, 1200)

    def today_coin(self):
        self.logger.info('获取今日金钱')
        time.sleep(random.random() + 1)
        self.pp(resourceId='com.tencent.weishi:id/qff').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp.xpath('//*[@resource-id="com.tencent.weishi:id/mcc"]/android.widget.FrameLayout[1]/'
                      'android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/'
                      'android.widget.RelativeLayout[1]').wait()
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.tencent.weishi:id/mcc"]/'
                                                 'android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/'
                                                 'android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]')
                                   .get().bounds)
        self.pp(description='任务中心').wait()
        self.pp(text='元').wait()
        time.sleep(random.random() + 1)
        coin = self.pp.xpath('//*[@text="元"]/preceding-sibling::android.view.View[1]').get_text()
        self.pp.press('back')
        time.sleep(random.random() + 1)
        if 'w' in coin:
            coin = int(float(coin.replace('w', '')) * 10000)
        else:
            print(coin)
            coin = float(coin)
        self.logger.info(f'今日已经获取金钱 {coin} 元')
        return coin

    def read_issue(self):
        read_issue_time = random.randint(3000, 4000)  # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time and self.today_coin() <= 0.5:
            self.read_issue_first()

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(resourceId='com.tencent.weishi:id/qfh').click(offset=(random.random(), random.random()))
        self.pp(resourceId='com.tencent.weishi:id/naw').wait()
        self.pp(resourceId='com.tencent.weishi:id/naw').click(offset=(random.random(), random.random()))
        self.pp(text="设置").wait()
        self.pp(text="设置").click(offset=(random.random(), random.random()))
        self.pp(text="清除缓存").wait()
        self.pp(text="清除缓存").click(offset=(random.random(), random.random()))

    def main_do(self):
        # raise
        self.app_start('微视')
        self.pp(resourceId='com.tencent.weishi:id/qfh').wait(timeout=30)
        self.read_issue()
        self.clean_cache()
        self.app_end()
