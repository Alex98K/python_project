from app_jiao_ben import AppReadBase
import random
import uiautomator2


class QuTouTiao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(QuTouTiao, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        
    def deng_lu(self):
        self.pp(text='我的').click(offset=(random.random(), random.random()))

    def main_do(self):
        self.app_start('趣头条')
        # 获取app权限，仅首次启动app才会用到
        # self.pp(text='同意').click_exists(timeout=3)
        # self.pp(text='同意去开启').click_exists(timeout=10)
        # self.pp(text='允许').click_exists(timeout=10)
        self.pp(text='我的').wait(timeout=30)
        self.deng_lu()

