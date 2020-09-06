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
        self.pp.watcher('tip2').when(xpath='//*[@resource-id="com.kuaiyin.player:id/ivDismiss"]').click()
        self.pp.watcher.start(0.5)

    def _read_issue_core(self, read_issue_time):
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
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
                    self.pp(resourceId='com.kuaiyin.player:id/submitInput')\
                        .click(offset=(random.random(), random.random()))
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

    def read_issue_first(self, duration, target_coin):
        self.logger.info(f'开始阅读主页')
        time.sleep(random.random() + 1)
        self.pp(text='主页').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        # 获取栏目
        lan_mu_num = self.pp(resourceId="com.kuaiyin.player:id/title_container").child().count
        random_list = [x for x in range(1, lan_mu_num)]
        random.shuffle(random_list)
        for j in random_list:
            t = time.time()
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
                read_issue_time = random.randrange(15, 185)  # 看文章的随机时间
                while time.time() - issue_time_start <= read_issue_time:
                    time.sleep(random.random())
                # 按照设定的点赞概率，随机点赞
                if self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/v_like"]').exists and \
                        random.random() < self.probability_thumb_up:
                    self.click_random_position(self.pp.xpath('//*[@resource-id="com.kuaiyin.player:id/v_like"]')
                                               .get().bounds)
                    time.sleep(random.random() + 1)
                time.sleep(random.random() + 3)
                # 随机跳过1-3次
                for k in range(random.randint(1, 3)):
                    self.pp(resourceId='com.kuaiyin.player:id/v_next').click(
                        offset=(random.random(), random.random()))
                    time.sleep(random.random())
                time.sleep(random.random() + 1)
            if time.time() - t > duration:
                self.logger.info(f'今日已经阅读了{duration}秒，不看了')
                return
            coin = self.today_coin()
            self.logger.info(f'已经获取了 {coin} 金币')
            if coin > target_coin:
                return
            else:
                self.click_random_position(self.pp.xpath('//*[@text="主页"]').get().bounds)
                time.sleep(random.random() + 1)
            self.logger.info('看完这个栏目了，换个栏目')

    def read_issue_city(self, read_issue_time):
        self.logger.info(f'开始阅读视频页')
        self.pp(text='视频').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self._read_issue_core(read_issue_time)

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

    def read_issue(self, duration, target_coin):
        read_issue_time = random.randint(300, 600)
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= duration and self.today_coin() <= target_coin:
            self.read_issue_first(duration, target_coin)
            if self.today_coin() > 10000:
                break
            self.read_issue_city(read_issue_time)

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('快音')
        self.pp(text='我的').wait(timeout=30)
        self.read_issue(duration, target_coin)
        self.app_end()
