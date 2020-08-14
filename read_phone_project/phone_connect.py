import uiautomator2
import os
import threading


class PhoneConnect(object):
    def __init__(self):
        self.phone_connects = {}
        self.connect()

    def one_connect(self, j):
        self.phone_connects[j] = uiautomator2.connect_usb(j)

    def connect(self):
        fp = os.popen('adb devices').readlines()
        job = []
        for j in fp:
            if 'device' in j and 'List' not in j:
                j = j.replace('device', '').strip()
                temp = threading.Thread(target=self.one_connect, args=(j,))
                temp.start()
                job.append(temp)
        for i in job:
            i.join()

    @property
    def connections(self):
        return self.phone_connects.values()

    @property
    def serials(self):
        return self.phone_connects.keys()

    @property
    def serials_connections(self):
        return self.phone_connects.items()

    def reboot_all(self):
        for k, v in self.phone_connects.items():
            try:
                v.shell('reboot')
            except RuntimeError:
                pass


if __name__ == '__main__':
    do = PhoneConnect()
    # do.reboot_all()
    print(do.serials_connections)
    # for k, v in do.serials_connections:
    #     print(v)
