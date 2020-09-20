import uiautomator2
from os import popen
from threading import Thread
import pathlib
import json


class PhoneConnect(object):
    def __init__(self):
        self.path = pathlib.Path().cwd()
        self.phone_connects = {}
        self.phone_connects_serials = []

    def one_connect(self, j):
        self.phone_connects[j] = uiautomator2.connect_usb(j)

    def connect_phone_serial(self):
        fp = popen('adb devices').readlines()
        for j in fp:
            if 'device' in j and 'List' not in j:
                j = j.replace('device', '').strip()
                if j == 'F7R0214305002612':
                    continue
                self.phone_connects_serials.append(j)

    def connect(self):
        fp = popen('adb devices').readlines()
        job = []
        for j in fp:
            if 'device' in j and 'List' not in j:
                j = j.replace('device', '').strip()
                temp = Thread(target=self.one_connect, args=(j,))
                temp.start()
                job.append(temp)
        for i in job:
            i.join()
        if not pathlib.Path.exists(self.path / 'conf'):
            pathlib.Path.mkdir(self.path / 'conf', parents=True)
        with open(self.path / 'conf/phone_connected_serials.json', 'w', encoding='UTF-8') as f:
            json.dump(list(self.serials), f)

    @property
    def connections(self):
        self.connect()
        return self.phone_connects.values()

    @property
    def serials(self):
        self.connect_phone_serial()
        return self.phone_connects_serials

    @property
    def serials_connections(self):
        self.connect()
        return self.phone_connects.items()

    def reboot_all(self):
        self.connect()
        for k, v in self.phone_connects.items():
            try:
                v.shell('reboot')
            except RuntimeError:
                pass

    def app_install(self, url=''):
        self.connect()
        for k, v in self.phone_connects.items():
            try:
                v.app_install(url)
            except RuntimeError:
                pass
            except OSError:
                print('请输出正确的app安装网址')

    def app_install_all(self):
        self.connect()
        with open(self.path / 'conf' / 'app_info.json', 'r', encoding='UTF-8') as f:
            app_info = json.load(f)
        for name, info in app_info.items():
            url = info[0]
            for k, v in self.phone_connects.items():
                if name not in v.app_list():
                    try:
                        print(f'准备给{k}安装app {info[1]}')
                        v.app_install(url)
                        print(f'已经给{k}安装了app {info[1]}')
                    except RuntimeError:
                        pass
                    except OSError:
                        print(f'安装{info[1]}出错，请配置正确的app安装网址')

    @staticmethod
    def test():
        pp = uiautomator2.connect_usb()
        # app_list = pp.app_list()
        # for j in app_list:
        #     try:
        #         print(pp.app_info(j))
        #     except uiautomator2.exceptions.BaseError:
        #         pass
        # print(app_list)
        print(pp.app_current())


if __name__ == '__main__':
    do = PhoneConnect()
    do.reboot_all()
    # print(do.serials_connections)
    # do.test()
    # do.app_install_all()
