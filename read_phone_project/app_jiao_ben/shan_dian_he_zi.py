from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class ShanDianHezi(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(ShanDianHezi, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when(xpath='//*[@resource-id="c.l.a:id/img_close"]').click()
        self.pp.watcher('tip2').when(xpath='//*[@resource-id="com.lechuan.mdwz:id/t"]').click()
        # self.pp.watcher('tip5').when(xpath='//*[@resource-id="com.cashtoutiao:id/iv_close"]').click()
        # self.pp.watcher('tip6').when(xpath='//*[@resource-id="com.cashtoutiao:id/tt_video_ad_close_layout"]').click()
        self.pp.watcher.start(0.5)

    def sign_in(self):
        self.logger.info(f'开始签到')
        self.pp(text='任务').wait()
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        if self.pp(text='立即签到').exists(timeout=5):
            self.pp(text='立即签到').click(offset=(random.random(), random.random()))

    def read_issue_first(self, read_issue_time, target_coin):
        self.logger.info(f'开始阅读首页视频')
        time.sleep(random.random() + 1)
        self.pp.xpath('//*[@resource-id="c.l.a:id/home_aggregation_recycler"]/android.widget.RelativeLayout[1]/'
                      'android.widget.TextView[1]').wait()
        self.click_random_position(self.pp.xpath('//*[@resource-id="c.l.a:id/home_aggregation_recycler"]/'
                                                 'android.widget.RelativeLayout[1]/'
                                                 'android.widget.TextView[1]').get().bounds)
        time.sleep(random.random() + 1)
        t = time.time()
        while time.time() - t < read_issue_time:
            # 每个栏目下的文章标题
            for title in self.pp.xpath('//*[@resource-id="c.l.a:id/title"]').all():
                time.sleep(random.random() + 1)
                # 需要满足看文章概率
                if random.random() >= self.probability_read_issue:
                    continue
                self.click_random_position(title.bounds)
                time.sleep(random.random() + 2)
                # 如果有获取金币的图标，才看，没有就返回,
                if not self.pp.xpath('//*[@resource-id="c.l.a:id/read_redpacket"]').exists:
                    while not self.pp(text='头条资讯').exists:
                        self.pp.press('back')
                        time.sleep(random.random() + 1)
                    continue
                self.app_switch_current()
                issue_time_start = time.time()  # 开始计时
                read_issue_time = random.randrange(5, 25)  # 看文章的随机时间
                read_video_time = random.randrange(5, 35)  # 看视频的随机时间
                # 按照设定的关注概率，随机关注
                if self.pp(resourceId="c.l.a:id/img_collect").exists and random.random() < self.probability_focus:
                    self.pp(resourceId="c.l.a:id/img_collect").click(offset=(random.random(), random.random()))
                    time.sleep(random.random() + 1)
                # 看下是视频还是文章，视频就停着看，文章就下滑看
                if self.pp.xpath('//*[@resource-id="c.l.a:id/vp_v_bg"]').exists:
                    while not (self.pp(text='重播').exists or time.time() - issue_time_start > read_video_time):
                        if self.pp(text='关闭广告').exists:
                            self.pp(text='关闭广告').click(offset=(random.random(), random.random()))
                        time.sleep(1)
                else:
                    while time.time() - issue_time_start <= read_issue_time:
                        time.sleep(random.uniform(3, 5))
                        self.scroll_read_issue()
                        if self.pp.xpath('//*[@content-desc="展开全文"]').exists:
                            self.click_random_position(self.pp.xpath('//*[@content-desc="展开全文"]').get().bounds)
                # 按照设定的点赞概率，随机点赞
                if self.pp.xpath('//*[@resource-id="c.l.a:id/img_like"]').exists and \
                        random.random() < self.probability_thumb_up:
                    self.click_random_position(self.pp.xpath('//*[@resource-id="c.l.a:id/img_like"]').get().bounds)
                    time.sleep(random.random() + 1)
                time.sleep(random.random() + 1)
                self.pp.press('back')
                time.sleep(random.random() + 1)
                if self.pp(resourceId='c.l.a:id/coin_tv').exists:
                    coin = self.pp(resourceId='c.l.a:id/coin_tv').get_text()
                    if '万' in coin:
                        coin = float(coin.replace('万', '')) * 10000
                    else:
                        coin = int(coin)
                    if coin > target_coin:
                        time.sleep(random.random() + 1)
                        self.pp.press('back')
                        time.sleep(random.random() + 1)
            # 随机下滑1-4次
            for k in range(random.randint(1, 4)):
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                time.sleep(random.random())
        if not self.pp(text='我的').exists:
            time.sleep(random.random() + 1)
            self.pp.press('back')
            time.sleep(random.random() + 1)

    def read_issue_city(self, read_issue_time):
        self.logger.info(f'开始阅读同城视频')
        self.pp(text='玩一玩').click(offset=(random.random(), random.random()))
        t = time.time()
        while time.time() - t < read_issue_time:
            self.scroll_read_issue()
            time.sleep(random.random() + 2)
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def read_issue(self, duration, target_coin):
        self.logger.info(f'开始阅读文章')
        time.sleep(random.random() + 1)
        self.pp.xpath('//*[@resource-id="c.l.a:id/bottom_navigation"]/android.widget.RelativeLayout[1]/'
                      'android.widget.RelativeLayout[1]').wait()
        self.click_random_position(self.pp.xpath('//*[@resource-id="c.l.a:id/bottom_navigation"]/'
                                                 'android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]')
                                   .get().bounds)
        time.sleep(random.random() + 1)
        if self.pp(text='领取奖励').exists:
            self.pp(text='领取奖励').click(offset=(random.random(), random.random()))
        read_issue_time1, read_issue_time2 = random.randint(600, 900), random.randint(300, 600)
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= duration and self.today_coin() <= target_coin:
            self.read_issue_first(read_issue_time1, target_coin)
            if self.today_coin() > target_coin:
                break
            self.read_issue_city(read_issue_time2)

    def today_coin(self):
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        coin = self.pp(resourceId='c.l.a:id/account_flash_cash').get_text() \
            .replace(' 金币', '').replace(',', '')
        time.sleep(random.random() + 1)
        self.pp(text='首页').wait()
        self.pp(text='首页').click(offset=(random.random(), random.random()))
        self.logger.info(f'已经获取 {coin} 金币')
        return int(coin)

    def cash_out(self, cash_out):
        if not cash_out:
            return
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(text='兑换提现').wait()
        self.pp(text='兑换提现').click(offset=(random.random(), random.random()))
        self.pp(text='提现方式').wait()
        time.sleep(random.random() + 1)
        coin = int(self.pp(resourceId='com.cashtoutiao:id/tv_tips_gold_coin').get_text()
                   .replace(' 金币', '').replace(',', ''))
        if coin >= 10000:
            self.pp(resourceId='com.cashtoutiao:id/rl_wechat').wait()
            self.pp(resourceId='com.cashtoutiao:id/rl_wechat').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
            self.pp(resourceId='com.cashtoutiao:id/item_view').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
            self.pp(resourceId='com.cashtoutiao:id/tv_withdraw').click(offset=(random.random(), random.random()))
        t = time.time()
        while not self.pp(text='我的').exists and time.time() - t < 60:
            self.pp.press('back')
            time.sleep(random.random() + 1)

    def coin2mb(self):
        self.pp(text='我的').wait()
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(text='我的余额').wait()
        self.pp(text='我的余额').click(offset=(random.random(), random.random()))
        self.pp(text='兑换现金').wait()
        self.pp(text='兑换现金').click(offset=(random.random(), random.random()))
        if self.pp(text='确定').exists(timeout=5):
            self.pp(text='确定').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('闪电盒子')
        self.pp(text='我的').wait(timeout=30)
        self.sign_in()
        self.read_issue(duration, target_coin)
        self.coin2mb()
        self.cash_out(cash_out)
        self.app_end()
