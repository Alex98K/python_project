import uiautomator2
import time
import random
import cv2
from my_module.PicMatch import PicMatchTemplate as pic

step = random.randint(10000, 12000)
print("今日刷步数%d" % step)
pp = uiautomator2.connect_usb('8DF6R16729018868')
# pp.screen_on()
# pp.open_identify()
# time.sleep(1.5)
# pp.click(0.482, 0.863)
# pp.click(0.496, 0.68)
# pp.click(0.482, 0.929)
# pp.click(0.859, 0.756)
# pp.click(0.169, 0.614)
# pp.click(0.169, 0.614)
# time.sleep(1)

pp.press('home')
time.sleep(1)
pp.swipe(300, 300, 100, 300)
time.sleep(1)
pp.app_start('com.Jshare.YunDong')
time.sleep(1)
if pp(resourceId='android:id/button3').exists:
    pp(resourceId='android:id/button3').click()
time.sleep(0.2)
if pp(text='切换：微信运动').exists:
    pp(text='切换：微信运动').click()
pp(resourceId="com.Jshare.YunDong:id/step").set_text(str(step))
pp(resourceId="com.Jshare.YunDong:id/ZhuoYiID").set_text("jiajia172000")
time.sleep(0.15)
if not pp(resourceId='com.Jshare.YunDong:id/submit').exists:
    pp.click(0.926, 0.558)
pp(resourceId='com.Jshare.YunDong:id/submit').click()
time.sleep(1.5)
pp.app_stop('com.Jshare.YunDong')
pp.press('home')
pp.screen_off()
