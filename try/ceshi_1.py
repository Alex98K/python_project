import uiautomator2
import time

# pp = uiautomator2.connect_usb()
pp = uiautomator2.connect_wifi('192.168.1.103')
# pp.screen_off()
pp.unlock()
print(pp.info)
