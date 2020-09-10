from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class WeiLiKanKan(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(WeiLiKanKan, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('继续观看').click()
        self.pp.watcher('tip2').when('立即领取').click()
        self.pp.watcher('tip3').when('没有邀请码').click()
        self.pp.watcher('tip4').when('继续阅读').click()
        self.pp.watcher.start(0.5)

    def sign_in(self):
        self.logger.info(f'开始签到')
        if self.pp(resourceId='cn.weli.story:id/rl_bottom_2').exists(timeout=5):
            self.pp(resourceId='cn.weli.story:id/rl_bottom_2').click(offset=(random.random(), random.random()))

    def _adjust_lan_mu(self):
        self.logger.info(f'开始调整栏目')
        lan_mu_num_end = len(self.pp.xpath('//*[@resource-id="cn.weli.story:id/indicator"]/'
                                           'android.widget.LinearLayout[1]//android.widget.FrameLayout').all()) - 1
        if lan_mu_num_end <= 5:
            return
        if self.pp(resourceId="cn.weli.story:id/iv_more").exists:
            self.pp(resourceId="cn.weli.story:id/iv_more").click(offset=(random.uniform(0.5, 0.9), random.random()))
            time.sleep(random.random() + 1)
        self.pp(text="编辑").wait()
        self.pp(text="编辑").click(offset=(random.uniform(0.5, 0.9), random.random()))
        time.sleep(random.random() + 1)
        for i in reversed(self.pp.xpath('//*[@resource-id="cn.weli.story:id/img_edit"]').all()):
            i.click()
            time.sleep(random.random() + 0.5)
        time.sleep(random.random() + 1)
        lan_mu_num = 2
        for j in reversed(self.pp.xpath('//*[@resource-id="cn.weli.story:id/tv_title"]').all()):
            if j.text not in ['三农', '萌宠'] and \
                    random.random() < 0.2 and lan_mu_num <= lan_mu_num_end:
                j.click()
                lan_mu_num += 1
                time.sleep(random.random() + 1)
        self.pp(text='完成').wait()
        self.pp(text='完成').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        self.pp.press('back')
        time.sleep(random.random() + 1)

    def read_issue(self, duration, target_coin):
        read_issue_time1, read_issue_time2 = random.randint(600, 900), random.randint(300, 600)
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= duration and self.today_coin() <= target_coin:
            self.read_issue_first(read_issue_time1, target_coin)
            if self.today_coin() > target_coin:
                break
            self.read_issue_city(read_issue_time2)

    def read_issue_first(self, read_issue_time2, target_coin):
        self.logger.info(f'开始阅读头条视频')
        time.sleep(random.random() + 1)
        self.pp(resourceId='cn.weli.story:id/rl_bottom_0').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        # 看情况调整栏目
        if self.pp.xpath('//*[@resource-id="cn.weli.story:id/indicator"]/android.widget.LinearLayout[1]/'
                         'android.widget.FrameLayout[last()]').get().bounds[2] >= \
                self.pp(resourceId="cn.weli.story:id/iv_more").bounds()[0]:
            self._adjust_lan_mu()
        # 获取栏目
        lan_mu_num = len(self.pp.xpath('//*[@resource-id="cn.weli.story:id/indicator"]/android.widget.LinearLayout[1]//'
                                       'android.widget.FrameLayout').all())
        random_list = [x for x in range(lan_mu_num)]
        random_list.pop(1)  # 删除第二个栏目序号
        random.shuffle(random_list)
        for j in random_list:
            t = time.time()
            self.click_random_position(self.pp.xpath(f'//*[@resource-id="cn.weli.story:id/indicator"]/'
                                                     f'android.widget.LinearLayout[1]/android.widget.FrameLayout'
                                                     f'[{j+1}]').get().bounds)
            time.sleep(random.random() + 1)
            for i in range(random.randint(8, 20)):  # 每个栏目下滑随机次
                # 每个栏目下的文章标题
                for title in self.pp.xpath('//*[@resource-id="cn.weli.story:id/tv_title"]').all():
                    # 需要满足看文章概率
                    if random.random() >= self.probability_read_issue:
                        continue
                    self.click_random_position(title.bounds)
                    time.sleep(random.random() + 2)
                    # 如果有获取金币的图标，才看，没有就返回,
                    if self.pp.xpath('//*[@resource-id="cn.weli.story:id/iv_coin"]').exists:
                        issue_time_start = time.time()  # 开始计时
                        read_issue_time = random.randrange(5, 25)  # 看文章的随机时间
                        read_video_time = random.randrange(5, 35)  # 看视频的随机时间
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
                                if self.pp.xpath('//*[@resource-id="cn.weli.story:id/tv_height_more"]').exists:
                                    self.click_random_position(self.pp.xpath('//*[@resource-id="cn.weli.story:id/'
                                                                             'tv_height_more"]').get().bounds)
                        # 按照设定的点赞概率，随机点赞
                        if self.pp.xpath('//*[@resource-id="cn.weli.story:id/btn_collect"]').exists and \
                                random.random() < self.probability_thumb_up:
                            self.click_random_position(self.pp.xpath('//*[@resource-id="cn.weli.story:id/btn_collect"]')
                                                       .get().bounds)
                            time.sleep(random.random() + 1)
                        time.sleep(random.random() + 1)
                        self.pp.press('back')
                        time.sleep(random.random() + 1)
                if time.time() - t > read_issue_time2:
                    self.logger.info(f'已经阅读了 {read_issue_time2} 秒，不看了')
                    return
                # 随机下滑2-4次
                for k in range(random.randint(1, 3)):
                    self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                  random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                    time.sleep(random.random())
            time.sleep(random.random() + 1)
            coin = self.today_coin()
            if coin > target_coin:
                self.logger.info(f'今日已经获取{coin}金币，不再阅读了')
                return
            else:
                self.click_random_position(self.pp.xpath('//*[@resource-id="cn.weli.story:id/rl_bottom_0"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
            self.logger.info('看完这个栏目了，换个栏目')

    def read_issue_city(self, read_issue_time):
        self.logger.info(f'开始阅读同城视频')
        self.pp(resourceId='cn.weli.story:id/rl_bottom_1').click(offset=(random.random(), random.random()))
        time.sleep(random.random() + 1)
        issue_time_start = time.time()  # 开始计时
        while time.time() - issue_time_start <= read_issue_time:
            time.sleep(random.uniform(3, 5))
            # 按照设定的点赞概率，随机点赞
            if self.pp.xpath('//*[@resource-id="cn.weli.story:id/iv_praise"]').exists and \
                    random.random() < self.probability_thumb_up:
                self.click_random_position(self.pp.xpath('//*[@resource-id="cn.weli.story:id/iv_praise"]')
                                           .get().bounds)
                time.sleep(random.random() + 1)
            self.scroll_read_issue()

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        t = time.time()
        while time.time() - t <= 60:
            if not self.pp(text="系统设置").exists:
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), steps=random.randint(20, 60))
                time.sleep(random.random())
            else:
                break
        self.pp(text="系统设置").click(offset=(random.random(), random.random()))
        self.pp(text="清除缓存").wait()
        self.pp(text="清除缓存").click(offset=(random.random(), random.random()))
        time.sleep(random.random())
        self.pp(text="清除中...").wait_gone()

    def today_coin(self):
        self.pp(resourceId='cn.weli.story:id/rl_bottom_4').wait()
        self.pp(resourceId='cn.weli.story:id/rl_bottom_4').click(offset=(random.random(), random.random()))
        self.pp(resourceId='cn.weli.story:id/text_today_coin').wait()
        time.sleep(random.random() + 1)
        coin = self.pp(resourceId='cn.weli.story:id/text_today_coin').get_text() \
            .replace(' 金币', '').replace(',', '')
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

    def main_do(self, duration, target_coin, cash_out):
        # raise
        self.app_start('微鲤看看')
        self.pp(resourceId='cn.weli.story:id/rl_bottom_4').wait(timeout=30)
        self.sign_in()
        self.read_issue(duration, target_coin)
        self.cash_out(cash_out)
        self.clean_cache()
        self.app_end()
