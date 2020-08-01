import uiautomator2
import time

pp = uiautomator2.connect_usb()
# pp.screen_on()
pp.unlock()
time.sleep(1)
img = pp.screenshot()
print(pp.window_size())
img2 = img.resize((720, 1080))

img2.show()
pp.screen_off()
