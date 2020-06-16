from my_module.PicMatch import PicMatchTemplate as pic
import time
import pytesseract
from my_module.pyauto import *
import cv2


# 系统中新建环境变量TESSDATA_PREFIX，为C:\Program Files\Tesseract-OCR\tessdata
# 重写tesseract.exe启动位置，无需设置环境变量
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
# windtitle = u'梦幻西游 ONLINE'
# time.sleep(2)
# screenshot()

pp = cv2.imread('screenshot.bmp', 0)
# cv2.imwrite('2.jpg', pp)
# text = pytesseract.image_to_string(pp, lang='chi_sim')
text1 = pytesseract.image_to_boxes(pp, lang='chi_sim')
print(text1)

# print(windowposition(windtitle))
# p1 = cv2.imread('windowscreenshot.bmp', 0)
# p2 = cv2.imread('3t.bmp', 0)
# t = pic(p1, p2)
# print(t)

# wind = win32gui.FindWindow(0, windtitle)
# win32gui.ShowWindow(wind, win32con.SW_SHOWNORMAL)
# win32gui.SetForegroundWindow(wind)
# time.sleep(0.3)
# inputkey(['alt','s'])
# mouseclick(100,300)

# print(windowall())
