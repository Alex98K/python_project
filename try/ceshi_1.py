import uiautomator2
import time, sys, traceback

# pp = uiautomator2.connect_usb()
# pp.shell('reboot')
# print(pp.address)
# pp.shell('reboot')
t = time.time()
f = open('error.txt', 'a+')
def had():
    a = [1, 2, 3]
    b = a[5]
    print(b)
def ok():
    had()
# try:
#     ok()
# except Exception as e:
#     print(e.__traceback__)
#     print(e.with_traceback(sys.exc_info()[2]))
#     print(traceback.print_exc(file=f))
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
while True:
    try:
        ok()
        break
    except Exception as e:
        traceback.print_exc()
        with open('error_log.txt', 'a+', encoding='UTF-8') as f3:
            f3.write(
                f'{traceback.print_exc(file=f3)}\n\n'
                     # f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n\n'
                     )
        # # self.pp.screenshot(f'出错啦，这是截图-error-错误码{e}-'
        # #                    f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.jpg')
        # if time.time() - t > 1:
        #     print('程序存在错误，试了一个小时都不行，请修改程序')
        #     # self.pp.app_stop('cn.xuexi.android')
        #     break
# pp = uiautomator2.connect_wifi('192.168.1.103')
# pp.screen_off()
# pp.unlock()
# print(pp.info)
