import pytesseract
from PIL import Image
import cv2


# 系统中新建环境变量TESSDATA_PREFIX，为C:\Program Files\Tesseract-OCR\tessdata
# 重写tesseract.exe启动位置，无需设置环境变量
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

pp = cv2.imread('screenshot.bmp', 1)
# pp = Image.open('windowscreenshot.bmp')
# print(pp)
text = pytesseract.image_to_string(pp, lang='chi_sim')

print(text)
