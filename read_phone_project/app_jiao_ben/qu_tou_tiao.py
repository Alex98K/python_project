from app_jiao_ben import AppReadBase
import uiautomator2


class QuTouTiao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(QuTouTiao, self).__init__(phone_serial, pp)
        self.pp = uiautomator2.connect_usb()
        
    def deng_lu(self):
        # self.pp
        pass

    def main_do(self):
        self.app_start('趣头条')
        self.pp(text=)

