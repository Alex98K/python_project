from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class KuaiYin(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(KuaiYin, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip4').when(xpath='//*[@resource-id="com.cashtoutiao:id/img_close"]').click()
        self.pp.watcher('tip1').when(xpath='//*[@resource-id="com.kuaiyin.player:id/w_v_back"]').click()
        # self.pp.watcher('tip1').when('我知道了').click()
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
            time.sleep(random.random() + 1)
        else:
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

    def _read_issue_core(self, time1, time2):
        read_issue_time = random.randint(time1, time2)  # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            # 如果不小心切换到了关注栏目，就回到推荐栏目
            # if self.pp.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/ax_"]').get().center()[0]\
            #         < self.pp(text='关注').bounds()[2]:
            #     self.pp(text='推荐').click(offset=(random.random(), random.random()))
            time.sleep(random.uniform(3, 10))
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/actionLike"]').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/actionLike"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
            # 按照设定的关注概率，随机关注
            if self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/videoFollow"]').exists and \
                    random.random() < self.probability_focus:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/videoFollow"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
            # 按照设定的评论概率，随机评论
            if self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/actionComment"]').exists and \
                    random.random() < self.probability_commit:
                self.click_random_position(self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/actionComment"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
                if self.pp(resourceId='com.kuaiyin.player:id/submitInput').exists:
                    self.pp(resourceId='com.kuaiyin.player:id/submitInput').click(offset=(random.random(), random.random()))
                self.pp(resourceId='com.kuaiyin.player:id/submitInput').wait()
                self.pp(resourceId='com.kuaiyin.player:id/submitInput').set_text(random.choice(self.commit))
                time.sleep(random.random() + 1)
                self.pp(resourceId='com.kuaiyin.player:id/submitRecord').wait()
                self.pp(resourceId='com.kuaiyin.player:id/submitRecord') \
                    .click(offset=(random.random(), random.random()))
                time.sleep(random.random() + 1)
                self.pp.press('back')
                time.sleep(random.random() + 1)
            self.scroll_read_issue()

    def read_issue_first(self):
        self.logger.info(f'开始阅读主页')
        time.sleep(random.random() + 1)
        self.pp(text='主页').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        # 获取栏目
        lan_mu_num = self.pp(resourceId="com.kuaiyin.player:id/title_container").child().count
        random_list = [x for x in range(1, lan_mu_num)]
        random.shuffle(random_list)
        for j in random_list:
            self.click_random_position(self.pp(resourceId="com.kuaiyin.player:id/title_container").child()[j].bounds())
            time.sleep(random.random() + 1)
            # 每个栏目下的文章标题
            self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/recyclerView"]/'
                          'android.widget.RelativeLayout').wait()
            self.click_random_position(self.pp.xpath(f'//*[@resource-id="com.kuaiyin.player:id/recyclerView"]/'
                                                     f'android.widget.RelativeLayout[{random.randint(1, 4)}]')
                                       .get().bounds)
            for i in range(random.randint(8, 12)):  # 每个栏目看随机多个音乐
                # 需要满足看文章概率
                if random.random() >= self.probability_read_issue:
                    self.pp(resourceId='com.kuaiyin.player:id/v_next').click(
                        offset=(random.random(), random.random()))
                    continue
                time.sleep(random.random() + 1)
                issue_time_start = time.time()  # 开始计时
                read_issue_time = random.randrange(5, 125, 30)  # 看文章的随机时间
                while time.time() - issue_time_start <= read_issue_time:
                    time.sleep(random.uniform(3, 5))
                # 按照设定的点赞概率，随机点赞
                if self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/v_like"]').exists and \
                        random.random() < self.probability_thumb_up:
                    self.click_random_position(self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/v_like"]')
                                               .get().bounds)
                    time.sleep(random.random() + 1)
                time.sleep(random.random() + 1)
                # 随机跳过1-3次
                for k in range(random.randint(1, 3)):
                    self.pp(resourceId='com.kuaiyin.player:id/v_next').click(
                        offset=(random.random(), random.random()))
                    time.sleep(random.random())
                time.sleep(random.random() + 1)
            coin = self.today_coin()
            self.logger.info(f'已经获取了 {coin} 金币')
            if coin > 10000:
                return
            else:
                self.click_random_position(self.pp.xpath('//*[@text="主页"]').get().bounds)
                time.sleep(random.random() + 1)
            self.logger.info('看完这个栏目了，换个栏目')

    def read_issue_city(self):
        self.logger.info(f'开始阅读视频页')
        self.pp(text='视频').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self._read_issue_core(600, 900)

    def today_coin(self):
        self.logger.info('获取今日金币数量')
        self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/tabIndicator"]/android.widget.RelativeLayout[3]').wait()
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/tabIndicator"]/'
                                                 'android.widget.RelativeLayout[3]').get().bounds)
        coin = self.pp.xpath('//*[@content-desc="现金收益"]/preceding-sibling::android.view.View[1]') \
            .get().attrib['content-desc'].replace(',', '').replace(' 兑换', '')
        time.sleep(random.random() + 1)
        if 'w' in coin:
            coin = int(float(coin.replace('w', '')) * 10000)
        else:
            coin = int(coin)
        self.logger.info(f'今日已经获取金币 {coin}')
        return coin

    def read_issue(self):
        read_issue_time = random.randint(3000, 4000)  # 看视频总时间
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time and self.today_coin() <= 10000:
            self.read_issue_first()
            if self.today_coin() > 10000:
                break
            self.read_issue_city()

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(resourceId='com.kuaiyin.player:id/setting').wait()
        self.pp(resourceId='com.kuaiyin.player:id/setting').click(offset=(random.random(), random.random()))
        self.pp(text="设置").wait()
        self.pp(text="设置").click(offset=(random.random(), random.random()))
        t = time.time()
        while time.time() - t > 60:
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

    def main_do(self):
        # raise
        self.app_start('快音')
        self.pp(text='我的').wait(timeout=30)
        # self.log_on()
        # self.sign_in()
        self.read_issue()
        # self.clean_cache()
        self.app_end()
