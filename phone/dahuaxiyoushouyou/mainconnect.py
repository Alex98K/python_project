import uiautomator2
import cv2
import requests
from lxml import etree
import pytesseract
from my_module.PicMatch import PicMatchTemplate
import time


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def connect():
    # laopo = '3EP7N18C11002513'
    # wode = '8DF6R16729018868'
    # jiushouji = 'F7R0214305002612'
    sanxing_pad = '0071ea56'
    # try:
    #     pp = uiautomator2.connect_usb(laopo)
    #     seial = laopo
    # except Exception:
    #     pass
    # try:
    #     pp = uiautomator2.connect_usb(wode)
    #     seial = wode
    # except Exception:
    #     pass
    # try:
    #     pp = uiautomator2.connect_usb(jiushouji)
    #     seial = jiushouji
    # except Exception as e:
    #     pass
    try:
        pp = uiautomator2.connect_usb(sanxing_pad)
        seial = sanxing_pad
    except Exception as e:
        pass
    # p1 = time.time()
    pp.screenshot("screen.jpg")
    # print(time.time()-p1)
    # pp.click(0.254, 0.07)
    # time.sleep(0.1)
    # pp.click(0.236, 0.689)
    # time.sleep(0.1)
    # pp.click(0.902, 0.144)
    return pp


if __name__ == '__main__':
    pp = connect()
    # img_title = cv2.imread("screen.jpg", 0)
    # img_left = cv2.imread("answer_left.jpg", 0)
    # answer_all = PicMatchTemplate(img_title, img_left)
    # print(answer_all)
    # text = pytesseract.image_to_string(img_title, lang='chi_sim')
    # print("识别的问题是\n", text)

