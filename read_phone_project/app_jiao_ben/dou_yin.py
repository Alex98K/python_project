from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class DouYin(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(DouYin, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        # self.pp.watcher('tip1').when('知道了').click()
        # self.pp.watcher('tip2').when('残忍离开').click()
        # self.pp.watcher.start(0.5)