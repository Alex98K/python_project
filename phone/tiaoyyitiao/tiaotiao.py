import aircv as ac
import cv2
import uiautomator2
import copy
import os
import time


class Tiao(object):
    def __init__(self):
        # self.pp = uiautomator2.connect_usb('0071ea56')
        self.pp = uiautomator2.connect_usb('8DF6R16729018868')
        # self.pp = uiautomator2.connect('192.168.1.218')
        # print(self.pp.window_size())

    def get_img_big(self):
        self.pp.screenshot("temp.jpg")
        self.im_big = cv2.imread('temp.jpg')  # 原始图像

    def find_pic(self):
        pic_files = os.listdir('./pic')
        qizi_position = dict()
        qizi_ps = tuple()
        im_big_cp = copy.deepcopy(self.im_big)
        for j in pic_files:
            im_small = cv2.imread(os.path.join('./pic', j))  # 带查找的部分
            # 在原图中查找小图位置并画方框保存
            all_pos = ac.find_all_template(self.im_big, im_small, threshold=0.6)
            if not all_pos:
                continue
            for i in all_pos:
                qizi_position = i['rectangle']
                qizi_ps = ((i['rectangle'][1][0] + i['rectangle'][3][0])//2, i['rectangle'][1][1])
                cv2.rectangle(im_big_cp, i['rectangle'][0], i['rectangle'][3], (255, 0, 0), 5)
            cv2.imwrite('recognize.jpg', im_big_cp)
        # print("棋子位置是", qizi_position)
        self.qizi_position = qizi_position
        return qizi_ps

    def gray_pic(self):
        # 灰度化处理
        # im_big_1 = cv2.imread('temp.jpg')
        # gray = cv2.cvtColor(im_big_1, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite('gay.jpg', gray)
        # ret, im_fixed = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
        # cv2.imwrite('2bina.jpg', im_fixed)
        pass

    def rage(self):
        img_blur = cv2.GaussianBlur(self.im_big, (3, 3), 0)  # 高斯模糊
        self.canny_img = cv2.Canny(img_blur, 50, 150)  # 边缘检测
        # cv2.namedWindow('img', cv2.WINDOW_KEEPRATIO)
        # cv2.imshow("img", self.canny_img)
        # cv2.waitKey(0)
        for y in range(self.qizi_position[0][0], self.qizi_position[3][0]):
            for x in range(self.qizi_position[0][1], self.qizi_position[3][1]):
                self.canny_img[x][y] = 0
        cv2.imwrite('cannoy.jpg', self.canny_img)

    def cut_pic(self):
        height, width = self.canny_img.shape
        self.crop_img = self.canny_img[500:height//2, 0:width]
        # cv2.namedWindow('img', cv2.WINDOW_KEEPRATIO)
        # cv2.imshow("img", self.crop_img)
        # cv2.waitKey(0)
        # cv2.imwrite('crop_img.jpg', self.crop_img)

    def center_ps(self):
        crop_h, crop_w = self.crop_img.shape
        center_x, center_y = 0, 0
        max_x = num_l = num_r = center_x_l = center_x_r = center_y_l = center_y_r = 0
        max_x_l = max_x_r = 0
        for y in range(crop_h):
            for x in range(self.qizi_position[0][0], crop_w):
                if self.crop_img[y, x] == 255:
                    if center_x_r == 0:
                        center_x_r = x
                    if x > max_x_r:
                        center_y_r = y
                        max_x_r = x
                    num_r += 1
            for x in range(self.qizi_position[0][0]):
                if self.crop_img[y, x] == 255:
                    if center_x_l == 0:
                        center_x_l = x
                    if x > max_x_l:
                        center_y_l = y
                        max_x_l = x
                    num_l += 1
            if num_l > num_r:
                center_x, center_y = center_x_l, center_y_l
            else:
                center_x, center_y = center_x_r, center_y_r
        # 下面代码是在图中标出中心点，白色圆心
        cv2.circle(self.crop_img, (center_x, center_y), 10, 255, -1)
        cv2.imwrite('center.jpg', self.crop_img)
        # cv2.namedWindow('img', cv2.WINDOW_KEEPRATIO)
        # cv2.imshow("img", self.crop_img)
        # cv2.waitKey(0)
        if center_y and center_x:
            return center_x, center_y
        else:
            print('中心点获取错误')
            raise

    def distance(self, qizi_x, qizi_y, center_x, center_y):
        return int(((qizi_x - center_x)**2 + (qizi_y - 10 - center_y)**2)**0.5)

    def press_go(self, dis):
        print(dis, 0.0006*dis)
        self.pp.long_click(900, 900, 0.0006*dis)

    def run(self):
        self.get_img_big()
        qizi_x, qizi_y = self.find_pic()
        self.gray_pic()
        self.rage()
        self.cut_pic()
        center_x, center_y = self.center_ps()
        dis = self.distance(qizi_x, qizi_y, center_x, center_y)
        self.press_go(dis)

    def go(self):
        while True:
            self.run()
            time.sleep(0.5)


if __name__ == '__main__':
    tiaotiao = Tiao()
    tiaotiao.go()








