import cv2
import os
import uiautomator2
from my_module.PicMatch import PicMatchTemplate as Pic

if __name__ == '__main__':
    # pp = uiautomator2.connect_usb('8DF6R16729018868')
    # pp = uiautomator2.connect_usb('0071ea56')
    # print(pp.window_size())
    # pp.screenshot("home.jpg")

    imsrc = cv2.imread('tiao2.jpg')
    # img_gray = cv2.cvtColor(imsrc, cv2.COLOR_BGR2GRAY)
    img_big = imsrc.copy()
    pic_files = os.listdir('./pic')
    for pic_name in pic_files:
        im_small = cv2.imread(os.path.join('./pic', pic_name))
        print(Pic(img_big, im_small))
