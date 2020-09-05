from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class QuTouTiao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(QuTouTiao, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('知道了').click()
        self.pp.watcher('tip2').when('残忍离开').click()
        self.pp.watcher('tip3').when('恭喜获得').press('back')
        self.pp.watcher.start(0.5)

    def today_coin(self):
        self.logger.info(f'获取今日金币数量')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        coin = self.pp.xpath('//*[@resource-id="com.jifen.qukan.personal:id/ea"]').get_text().replace(' 今日金币', '')
        return int(coin)

    def sign_in(self):
        self.logger.info(f'开始签到')
        if self.pp(text='签到').exists(timeout=5):
            self.pp(text='签到').click(offset=(random.random(), random.random()))

    def _adjust_lan_mu(self):
        self.logger.info(f'开始调整栏目')
        lan_mu_num_end = self.pp(resourceId="com.jifen.qukan:id/bfn").count - 1
        if lan_mu_num_end <= 6:
            return
        if self.pp(resourceId="com.jifen.qukan:id/ada").exists:
            self.pp(resourceId="com.jifen.qukan:id/ada").click(offset=(random.uniform(0.5, 0.9), random.random()))
            time.sleep(random.random() + 1)
            self.pp(text='编辑').wait()
            self.pp(text='编辑').click(offset=(random.random(), random.random()))
        lan_mu_num = 0
        for j in reversed(self.pp(resourceId='com.jifen.qukan:id/aoa')):
            if j.get_text() in ['小剧场', '小视频', '直播', '好货', '小说', '抗疫', '视频', '北京'] or \
                    random.random() < 0.7 or lan_mu_num >= lan_mu_num_end:
                j.sibling(resourceId='com.jifen.qukan:id/aob').click_exists()
            else:
                lan_mu_num += 1
        self.pp(text='完成').wait()
        self.pp(text='完成').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def read_issue(self, duration, target_coin):
        self.logger.info(f'开始阅读文章')
        time.sleep(random.random() + 1)
        self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/n9"]/android.widget.FrameLayout[1]').wait()
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/n9"]/'
                                                 'android.widget.FrameLayout[1]').get().bounds)
        if self.pp(text='领取').exists(timeout=3):
            self.pp(text='领取').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        # 看情况调整栏目
        if self.pp(resourceId="com.jifen.qukan:id/bfn")[-1].bounds()[2] > \
                self.pp(resourceId="com.jifen.qukan:id/ada").bounds()[0]:
            self._adjust_lan_mu()
        # 获取栏目
        lan_mu_num = self.pp(resourceId="com.jifen.qukan:id/bfn").count
        random_list = [x for x in range(lan_mu_num)]
        random.shuffle(random_list)
        for j in random_list:
            t = time.time()
            self.click_random_position(self.pp(resourceId="com.jifen.qukan:id/bfn")[j].bounds())
            time.sleep(random.random() + 1)
            for i in range(random.randint(8, 12)):  # 每个栏目下滑随机次
                # 每个栏目下的文章标题
                for title in self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/al8"]').all():
                    # 需要满足看文章概率
                    if random.random() >= self.probability_read_issue:
                        continue
                    self.click_random_position(title.bounds)
                    time.sleep(random.random() + 1)
                    # 如果有获取金币的图标，才看，没有就返回,
                    if self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/a3_"]').exists:
                        issue_time_start = time.time()  # 开始计时
                        read_issue_time = random.randrange(5, 125, 30)  # 看文章的随机时间
                        read_video_time = random.randrange(5, 185, 30)  # 看视频的随机时间
                        # 看下是视频还是文章，视频就停着看，文章就下滑看
                        if self.pp.xpath('//com.qukan.media.player.renderview.TextureRenderView').exists:
                            while not (self.pp(text='重播').exists or time.time() - issue_time_start > read_video_time):
                                if self.pp(text='关闭广告').exists:
                                    self.pp(text='关闭广告').click(offset=(random.random(), random.random()))
                                time.sleep(1)
                        else:
                            while time.time() - issue_time_start <= read_issue_time:
                                time.sleep(random.uniform(3, 5))
                                self.scroll_read_issue()
                                if not self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/g3"]').exists:
                                    self.pp.press('back')
                        # 按照设定的点赞概率，随机点赞
                        if self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bla"]').exists and \
                                random.random() < self.probability_thumb_up:
                            self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bla"]')
                                                       .get().bounds)
                            time.sleep(random.random() + 1)
                        # 按照设定的关注概率，随机关注
                        if self.pp(description="关注").exists and random.random() < self.probability_focus:
                            self.pp(description="关注").click(offset=(random.random(), random.random()))
                            time.sleep(random.random() + 1)
                        # 按照设定的评论概率，随机评论
                        if self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bku"]').exists and \
                                random.random() < self.probability_commit:
                            while True:
                                self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bku"]')
                                                           .get().bounds)
                                time.sleep(random.random() + 1)
                                if self.pp(text='我来说两句...').exists:
                                    self.pp(text='我来说两句...').click(offset=(random.random(), random.random()))
                                    break
                                elif self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/zq"]').exists:
                                    break
                            self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/zq"]').wait()
                            self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/zq"]'). \
                                set_text(random.choice(self.commit))
                            time.sleep(random.random() + 1)
                            self.pp(text='发布').click(offset=(random.random(), random.random()))
                            time.sleep(random.random() + 1)
                    time.sleep(random.random() + 1)
                    self.pp.press('back')
                    time.sleep(random.random() + 1)
                if time.time() - t > duration:
                    self.logger.info(f'已经阅读了 {duration} 秒，不看了')
                    return
                if not self.pp(text='我的').exists:
                    self.pp.press('back')
                    time.sleep(random.random() + 1)
                # 随机下滑2-4次
                for k in range(random.randint(2, 4)):
                    self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                  random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                    time.sleep(random.random())
            time.sleep(random.random() + 1)
            coin = self.today_coin()
            if coin > target_coin:
                self.logger.info(f'今日已经获取{coin}金币，不再阅读了')
                return
            else:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/n9"]/'
                                                         'android.widget.FrameLayout[1]').get().bounds)
                time.sleep(random.random() + 1)
            self.logger.info('看完这个栏目了，换个栏目')

    def get_read_reward(self):
        self.logger.info(f'开始获阅读文章的奖励')
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        t = time.time()
        while time.time() - t <= 300:
            t1 = time.time()
            while time.time() - t1 <= 60:
                if not self.pp(text="阅读得大额奖励").exists or self.pp(text="阅读得大额奖励").center()[1] > \
                        self.pp.xpath('//*[@resource-id="com.jifen.qukan.taskcenter:id/g5"]').get().bounds[1]:
                    self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                  random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                    time.sleep(random.random())
                else:
                    break
            temp = self.pp.xpath('//*[@text="阅读得大额奖励"]/following-sibling::android.widget.TextView[3]')
            if temp.get_text() == '领取奖励':
                self.click_random_position(temp.get().bounds)
                if self.pp(text='关闭').exists(timeout=60):
                    self.pp(text='关闭').click(offset=(random.random(), random.random()))
                    time.sleep(random.random() + 1)
                self.pp.press('back')
                if self.pp.xpath('com.jifen.qukan:id/tt_video_ad_close_layout').exists:
                    self.click_random_position(self.pp.xpath('com.jifen.qukan:id/tt_video_ad_close_layout')
                                               .get().bounds)
                if self.pp(text='恭喜获得').exists(timeout=3):
                    self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan.taskcenter:id/r"]')
                                               .get().bounds)
            else:
                break

    def get_advertisement_reward(self):  # 看广告的金币，收益低
        self.logger.info(f'开始看广告获金币')
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        t = time.time()
        while time.time() - t <= 300:
            t1 = time.time()
            while time.time() - t1 <= 60:
                if not self.pp(text="看广告视频拿金币").exists or self.pp(text="阅读得大额奖励").center()[1] > \
                            self.pp.xpath('//*[@resource-id="com.jifen.qukan.taskcenter:id/g5"]').get().bounds[1]:
                    self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                  random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                    time.sleep(random.random())
                else:
                    break
            temp = self.pp.xpath('//*[@text="看广告视频拿金币"]/following-sibling::android.widget.TextView[2]')
            if temp.get_text() == '立即观看':
                self.click_random_position(temp.get().bounds)
                if self.pp(text='关闭').exists(timeout=60):
                    self.pp(text='关闭').click(offset=(random.random(), random.random()))
                time.sleep(random.random() + 1)
                self.pp.press('back')
                if self.pp.xpath('com.jifen.qukan:id/tt_video_ad_close_layout').exists:
                    self.click_random_position(self.pp.xpath('com.jifen.qukan:id/tt_video_ad_close_layout')
                                               .get().bounds)
                if self.pp(text='恭喜获得').exists(timeout=3):
                    self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan.taskcenter:id/r"]')
                                               .get().bounds)
                time.sleep(random.random() + 1)
            else:
                break

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
        self.pp(text="清除缓存").wait()
        self.pp(text="清除缓存").click(offset=(random.random(), random.random()))

    def cash_out(self):
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(text='我的金币').wait()
        self.pp(text='我的金币').click(offset=(random.random(), random.random()))
        self.pp(description='提现').wait()
        self.pp(description='提现').click(offset=(random.random(), random.random()))

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('趣头条')
        # 过了开头的广告动画
        self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/pe"]').wait()
        self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/pe"]').wait_gone()
        self.pp(text='我的').wait(timeout=30)
        coin = self.today_coin()
        self.sign_in()
        if coin < target_coin:
            self.read_issue(duration, target_coin)
        else:
            self.logger.info(f'今日已经获取{coin}金币，不再阅读了')
        self.get_read_reward()
        self.get_advertisement_reward()
        self.clean_cache()
        self.app_end()
