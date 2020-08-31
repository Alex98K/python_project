from time import sleep


class CleanCash(object):
    def __init__(self, pp):
        self.pp = pp

    def main_do(self):
        self.pp.press('home')
        self.pp.app_stop_all(excludes=['com.dolby', 'com.mediatek.nlpservice', 'com.android.music', 'se.dirac.acs',
                                       'com.tencent.android.location', 'com.android.phone', 'com.android.systemui',
                                       'com.android.launcher3', 'com.letv.android.euiadplugin', 'com.letv.domain',
                                       'com.mediatek.ims', 'com.letv.android.freeflow', 'com.goodix.fingerprint',
                                       'com.android.deskclock', 'com.android.inputmethod.latin', 'com.stv.stvpush',
                                       'com.letv.android.usagestats', 'com.letv.android.phonecontrol',
                                       'com.letv.agnes', 'com.github.uiautomator', 'com.mediatek.gba'])
        self.pp.app_start('com.letv.android.supermanager',
                          'com.letv.android.supermanager.activity.RubbishCleanActivity')
        self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').wait()
        while self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').get_text()[0] != '一':
            sleep(1)
        self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').click()
        self.pp(resourceId='com.letv.android.supermanager:id/deepScanButton').wait()
        self.pp(resourceId='com.letv.android.supermanager:id/deepScanButton').click()
        self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').wait()
        while self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').get_text()[0] != '一':
            sleep(1)
        self.pp(resourceId='com.letv.android.supermanager:id/bottomButton').click()
        self.pp.app_stop('com.letv.android.supermanager')
