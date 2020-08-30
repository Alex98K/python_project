from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class KuaiShou(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(KuaiShou, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        # self.pp.watcher('tip1').when('我知道了').click()
        # self.pp.watcher('tip2').when('残忍离开').click()
        # self.pp.watcher.start(0.5)


    def main_do(self):
        # raise
        self.app_start('快手极速版')
        self.pp(text='我').wait(timeout=30)
        self.log_on()
        self.sign_in()
        self.read_issue()
        self.clean_cache()
        # self.coin_info()
        self.app_end()