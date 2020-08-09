import uiautomator2
import time, sys, traceback

# pp = uiautomator2.connect_usb()
# pp.shell('reboot')
# print(pp.address)
# pp.shell('reboot')
f = open('error.txt', 'a+')
def had():
    a = [1, 2, 3]
    b = a[5]
    print(b)
def ok():
    had()
try:
    ok()
except Exception as e:
    print(e.__traceback__)
    print(e.with_traceback(sys.exc_info()[2]))
    print(traceback.print_exc(file=f))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
# pp = uiautomator2.connect_wifi('192.168.1.103')
# pp.screen_off()
# pp.unlock()
# print(pp.info)
