from app_jiao_ben import AppReadBase
import random
import uiautomator2


class QuTouTiao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(QuTouTiao, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        
    def sign_in(self):
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        if self.pp(text='登录').exists(timeout=5):
            self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bnl"]').click_exists(timeout=20)
        else:
            return

    def qian_dao(self):
        self.pp(text='签到').click(offset=(random.random(), random.random()))
        if self.pp(text='恭喜获得').exists(timeout=3):
            self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/wj"]').click(offset=(random.random(), random.random()))

    def jurisdiction(self):
        # 需要获取电话权限、通知权限
        # 获取app权限，仅首次启动app才会用到
        if self.pp(text='同意').exists(timeout=3):
            self.pp(text='同意').click_exists(timeout=3)
            self.pp(text='同意去开启').click_exists(timeout=10)
            self.pp(text='允许').click_exists(timeout=10)

    def main_do(self):
        self.qian_dao()
        raise
        self.app_start('趣头条')
        self.jurisdiction()
        self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/pe"]').wait()
        self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/pe"]').wait_gone()
        self.pp(text='我的').wait(timeout=30)
        self.sign_in()

