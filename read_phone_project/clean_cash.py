import time
import uiautomator2


class CleanCash(object):
    def __init__(self, pp):
        self.pp = pp
        self.exclude = ['com.dolby', 'com.mediatek.nlpservice', 'com.android.music', 'se.dirac.acs',
                        'com.tencent.android.location', 'com.android.phone', 'com.android.systemui',
                        'com.android.launcher3', 'com.letv.android.euiadplugin', 'com.letv.domain',
                        'com.mediatek.ims', 'com.letv.android.freeflow', 'com.goodix.fingerprint',
                        'com.android.deskclock', 'com.android.inputmethod.latin', 'com.stv.stvpush',
                        'com.letv.android.usagestats', 'com.letv.android.phonecontrol',
                        'com.letv.agnes', 'com.github.uiautomator', 'com.mediatek.gba']

    def main_do(self):
        self.pp.press('home')
        self.pp.app_stop_all(excludes=self.exclude)
        self.pp.app_start('com.letv.android.supermanager',
                          'com.letv.android.supermanager.activity.RubbishCleanActivity')
        self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').wait()
        while self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').get_text()[0] != '一':
            time.sleep(1)
        self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').click()
        self.pp(resourceId='com.letv.android.supermanager:id/deepScanButton').wait()
        self.pp(resourceId='com.letv.android.supermanager:id/deepScanButton').click()
        self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').wait()
        while self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').get_text()[0] != '一':
            time.sleep(1)
        t = time.time()
        while time.time() - t < 20:
            for j in self.pp.xpath('//*[@resource-id="com.letv.android.supermanager:id/rubbishCleanListView"]//'
                                   'android.widget.RelativeLayout/com.letv.shared.widget.LeCheckBox[1]').all():
                img = j.screenshot()
                r, g, b = img.resize((1, 1)).getpixel((0, 0))
                if r > 200 and g > 200 and b > 200:
                    j.click()
            self.pp.swipe(0.3, 0.7, 0.3, 0.2, steps=60)
            time.sleep(1)
        self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').click()
        self.pp.app_stop('com.letv.android.supermanager')

    def app_init(self):
        self.pp.press('home')
        self.pp.app_stop_all(excludes=self.exclude)


if __name__ == '__main__':
    CleanCash(uiautomator2.connect_usb()).main_do()
