import uiautomator2
import cv2
import requests
from lxml import etree
import pytesseract
from selenium import webdriver
from my_module.PicMatch import PicMatchTemplate


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
textlength = 20
seial = None


def connect():
    laopo = '3EP7N18C11002513'
    wode = '8DF6R16729018868'
    try:
        pp = uiautomator2.connect_usb(laopo)
        seial = laopo
    except Exception:
        try:
            pp = uiautomator2.connect_usb(wode)
            seial = wode
        except Exception as e:
            raise e
    pp.screenshot("screen.jpg")
    im_big = cv2.imread('screen.jpg', 1)
    width = im_big.shape[1]
    height = im_big.shape[0]
    if seial == wode:
        widthx1 = height*650//2560
        widthx2 = height*1050//2560
        heighty1 = width*100//1440
        heighty2 = width*1325//1440
    elif seial == laopo:
        widthx1 = height*600//3120
        widthx2 = height*1000//3120
        heighty1 = width*100//1440
        heighty2 = width*1000//1440
    else:
        raise ()
    img_title = im_big[widthx1:widthx2, heighty1:heighty2]
    cv2.imwrite("1.jpg", img_title)


connect()

# img_left = cv2.imread("left.jpg", 1)
# hl, wl, tl = img_left.shape
# img_right = cv2.imread("right.jpg", 1)
# hr, wr, tr = img_right.shape
# rest_left = PicMatchTemplate(im_big, img_left)
# rest_right = PicMatchTemplate(im_big, img_right)
# a_leftup = (rest_left[0][0]-wl//2, rest_left[0][1]-hl//2)
# a_rightdown = (rest_right[0][0]+wr//2, rest_right[0][1]+hr//2)
# b_leftup = (rest_left[1][0]-wl//2, rest_left[1][1]-hl//2)
# b_rightdown = (rest_right[1][0]+wr//2, rest_right[1][1]+hr//2)
# c_leftup = (rest_left[2][0]-wl//2, rest_left[2][1]-hl//2)
# c_rightdown = (rest_right[2][0]+wr//2, rest_right[2][1]+hr//2)
# d_leftup = (rest_left[3][0]-wl//2, rest_left[3][1]-hl//2)
# d_rightdown = (rest_right[3][0]+wr//2, rest_right[3][1]+hr//2)
# print(a_leftup, a_rightdown, b_leftup, b_rightdown, c_leftup, c_rightdown, d_leftup, d_rightdown)
# img_a = im_big[a_leftup[1]:a_rightdown[1], a_leftup[0]:a_rightdown[0]]
# cv2.imwrite("img_a.jpg", img_a)

# img_a1 = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
# ret, img_a2 = cv2.threshold(img_a1, 127, 255, cv2.THRESH_BINARY)
# text2 = pytesseract.image_to_string(img_a2, lang='chi_sim')
# print(text2)

# text1 = pytesseract.image_to_boxes(img_title, lang='chi_sim')
# print(text1)

img_title = cv2.imread("1.jpg", 0)
text = pytesseract.image_to_string(img_title, lang='chi_sim')
text = text.replace("?", "？").replace("|", "").replace(" ", "").replace("\n", "").replace(",", "，").replace("】", "").replace("【", "").replace("(", "").replace(")", "")
print("识别的问题是\n", text)
haders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
url_answer = None
for i in range(textlength-2):
    url_question = "http://www.okkkj.cn/?q={}".format(text[:textlength-i])
    res_question = requests.get(url_question, headers=haders)
    html_question = etree.HTML(res_question.content.decode())
    try:
        url_answer = html_question.xpath('/html/body//ul[@class="nav"]/li[1]//a/@href')[0]
        break
    except IndexError:
        pass
if not url_answer:
    print('没有找到答案，百度一下')
    driver = webdriver.Chrome()
    # driver.maximize_window()
    driver.get(u"https://www.baidu.com")
    driver.find_element_by_id("kw").send_keys(text)
    driver.find_element_by_id("su").click()
    raise()
res_answer = requests.get(url_answer, headers=haders)
html_answer = etree.HTML(res_answer.content.decode())
answer = html_answer.xpath('//div[@class="row question-des"]//span[contains(@style,"background-color")]//text()')
answer_all = html_answer.xpath('//div[@class="row question-des"]//span[contains(@style,"font")]//text()')
# answer_all = html_answer.xpath('//div[@class="row question-des"]//span[position()<=2]//text()')
print("找到的全部答案是\n", answer_all)
print("找到的答案是\n", "".join(answer))
# answer_pos = answer_all.index(answer[0])
# print(len(answer_all), answer_pos)

