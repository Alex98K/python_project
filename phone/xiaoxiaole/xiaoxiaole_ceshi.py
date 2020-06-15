import uiautomator2
from PIL import Image
import cv2
import numpy


# pp = uiautomator2.connect_usb('8DF6R16729018868')
pp = uiautomator2.connect_usb('0071ea56')
print(pp.window_size())
# print(pp.dump_hierarchy())

# 截取并保存到计算机上的文件，需要Android> = 4.2。
pp.screenshot("tiao2.jpg")
# 得到PIL.Image格式的图像. 但你必须先安装pillow
# image = pp.screenshot()
# default format="pillow"
# image.save("home.jpg")
# or home.png. Currently, 只支持png and jpg格式的图像
# 得到OpenCV的格式图像。当然，你需要numpy和cv2安装第一个
# image = pp.screenshot(format='opencv')
# cv2.imwrite('home.jpg', image)
# 获取原始JPEG数据
# imagebin = pp.screenshot(format='raw')
# open("some.jpg", "wb").write(imagebin)
