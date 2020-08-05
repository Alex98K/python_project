import uiautomator2
import time

pp = uiautomator2.connect_usb()
# pp.screen_on()
pp.unlock()
# time.sleep(1)
# pp.unlock()
pp.toast.show("Hello world", 5.0)
print(pp.toast.get_message())
pp.toast.reset()
pp.watcher.stop()
pp.watcher.remove()
# img = pp.screenshot()
# print(pp.window_size())
# img2 = img.resize((720, 1080))

# img2.show()
# pp.screen_off()
