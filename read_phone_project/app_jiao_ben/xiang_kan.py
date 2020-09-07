from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class XiangKan(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(XiangKan, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('我知道了').click()
        self.pp.watcher('tip2').when(xpath='//*[@resource-id="com.xiangkan.android:id/iv_close"]').click()
        self.pp.watcher('tip3').when(xpath='//*[@resource-id="com.xiangkan.android:id/closeIv"]').click()
        self.pp.watcher.start(0.5)

    def sign_in(self):
        self.logger.info(f'开始签到')
        if self.pp(text='签到').exists(timeout=5):
            self.pp(text='签到').click(offset=(random.random(), random.random()))

    def read_issue(self, duration, target_coin):
        self.logger.info(f'开始阅读文章')
        time.sleep(random.random() + 1)
        self.pp(text='首页').wait()
        self.pp(text='首页').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        t = time.time()
        read_video_num = 0
        while True:
            for title in self.pp(resourceId='com.xiangkan.android:id/iv_video_cover'):
                time.sleep(random.random() + 1)
                # 需要满足看文章概率
                if random.random() >= self.probability_read_issue:
                    continue
                self.click_random_position(title.bounds())
                time.sleep(random.random() + 2)
                read_video_num += 1
                issue_time_start = time.time()  # 开始计时
                read_video_time = random.randrange(5, 185)  # 看视频的随机时间
                # 按照设定的关注概率，随机关注
                if self.pp(text="关注").exists and random.random() < self.probability_focus:
                    self.pp(text="关注").click(offset=(random.random(), random.random()))
                    time.sleep(random.random() + 1)
                # 看视频
                while not (self.pp(resourceId='com.xiangkan.android:id/tv_close_ad').exists or
                           time.time() - issue_time_start > read_video_time):
                    if self.pp(text='关闭广告').exists:
                        self.pp(text='关闭广告').click(offset=(random.random(), random.random()))
                    time.sleep(1)
                # 按照设定的点赞概率，随机点赞
                if self.pp.xpath('//*[@resource-id="com.xiangkan.android:id/img_thumbUp"]').exists and \
                        random.random() < self.probability_thumb_up:
                    self.click_random_position(self.pp.xpath('//*[@resource-id="com.xiangkan.android:id/'
                                                             'img_thumbUp"]').get().bounds)
                    time.sleep(random.random() + 1)
                # 按照设定的评论概率，随机评论
                if self.pp.xpath('//*[@resource-id="com.xiangkan.android:id/add_comments"]').exists and \
                        random.random() < self.probability_commit:
                    self.click_random_position(self.pp.xpath('//*[@resource-id="com.xiangkan.android:id/'
                                                             'add_comments"]').get().bounds)
                    time.sleep(random.random() + 1)
                    self.pp(resourceId='com.xiangkan.android:id/et_comment').wait()
                    self.pp(resourceId='com.xiangkan.android:id/et_comment').set_text(random.choice(self.commit))
                    time.sleep(random.random() + 1)
                    self.pp(text='发布').click(offset=(random.random(), random.random()))
                    time.sleep(random.random() + 1)
                    self.pp.press('back')
                time.sleep(random.random() + 1)
                self.pp.press('back')
                if read_video_num % 5 == 0:
                    time.sleep(random.random() + 1)
                    coin = self.today_coin()
                    if time.time() - t > duration:
                        self.logger.info(f'今日阅读时间超过了{duration}秒，不再阅读了')
                        return
                    elif coin > target_coin:
                        self.logger.info(f'今日获取金币超过 {coin} ，不在阅读了')
                        return
                    else:
                        self.pp(text='首页').wait()
                        self.pp(text='首页').click(offset=(random.random(), random.random()))
                        time.sleep(random.random() + 1)
            # 随机下滑2-4次
            for k in range(random.randint(2, 4)):
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                time.sleep(random.random())

    def today_coin(self):
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(text='任务中心').wait()
        self.pp(text='任务中心').click(offset=(random.random(), random.random()))
        self.pp(resourceId='com.xiangkan.android:id/user_center_coinnum_text').wait()
        time.sleep(random.random() + 1)
        coin = self.pp(resourceId='com.xiangkan.android:id/user_center_coinnum_text').get_text().replace('我的金币', '')
        self.pp.press('back')
        time.sleep(random.random() + 1)
        self.logger.info(f'今日已经获取 {coin} 个金币')
        return int(coin)

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('想看资讯')
        self.pp(text='我的').wait(timeout=30)
        if self.today_coin() < target_coin:
            self.read_issue(duration, target_coin)
        else:
            self.logger.info(f'今日已经获取超过10000个金币，不再阅读了')
        self.app_end()
