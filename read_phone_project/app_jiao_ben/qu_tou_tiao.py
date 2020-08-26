from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class QuTouTiao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(QuTouTiao, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('知道了').press()
        self.pp.watcher.start(0.5)

    def jurisdiction(self):
        # 需要获取电话权限、通知权限
        # 获取app权限，仅首次启动app才会用到
        if self.pp(text='同意').exists(timeout=3):
            self.pp(text='同意').click_exists(timeout=3)
            self.pp(text='同意去开启').click_exists(timeout=10)
            self.pp(text='允许').click_exists(timeout=10)
        
    def sign_in(self):
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        if self.pp(text='登录').exists(timeout=5):
            self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bnl"]').click_exists(timeout=20)
        else:
            return

    def qian_dao(self):
        self.pp(text='签到').click(offset=(random.random(), random.random()))
        if self.pp(text='恭喜获得').exists(timeout=3):
            self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/wj"]').click()

    def read_issue(self):
        self.pp(text='刷新').click(offset=(random.random(), random.random()))
        if self.pp(text='领取').exists:
            self.pp(text='领取').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
        # 获取栏目
        for lan_mu in self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/ad_"]/android.widget.LinearLayout[1]//'
                                    'android.widget.RelativeLayout').all()[1:]:
            self.click_random_position(lan_mu.bounds)
            time.sleep(random.random() + 1)
            for i in range(random.randint(5, 10)):  # 每个栏目下滑5-10次
                # 每个栏目下的文章标题
                for title in self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/al8"]').all():
                    self.click_random_position(title.bounds)
                    issue_time_start = time.time()
                    while True:
                        time.sleep(random.uniform(5, 8))
                        self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                      random.uniform(0.2, 0.3), random.uniform(0.2, 0.5))
                        # self.pp(scrollable=True).scroll(steps=200)
                        if time.time() - issue_time_start > 40:
                            break


            self.pp(scrollable=True).scroll(steps=90)




    def main_do(self):
        self.read_issue()
        raise
        self.app_start('趣头条')
        self.jurisdiction()
        self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/pe"]').wait()
        self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/pe"]').wait_gone()
        self.pp(text='我的').wait(timeout=30)
        self.sign_in()
        self.qian_dao()


