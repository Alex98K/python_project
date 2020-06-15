import cv2
import os
import uiautomator2
import numpy as np
from multiprocessing import Process


def match_pic(img_big, im_small, meth, pic_name):
    img = img_big.copy()
    method = eval(meth)
    t, w, h = im_small.shape[::-1]
    res = cv2.matchTemplate(img, im_small, method)
    # print(res)
    threshold = 0.8
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(min_val, max_val, min_loc, max_loc)
    loc = np.where(res >= threshold)
    # print(loc)
    result = []
    for pt in zip(*loc[::-1]):
        # print(pt)
        if result:
            for index, i in enumerate(result):
                if (i[0] <= (pt[0] + w//2) <= i[0] + w) and (i[1] <= (pt[1] + h//2) <= i[1] + h):
                    break
                else:
                    if index == len(result) - 1:
                        result.append(pt)
        else:
            result.append(pt)
    print(result)
    for p in result:
        cv2.rectangle(img, (p[0], p[1]), (p[0] + w, p[1] + h), (0, 0, 255), 3)
    cv2.imwrite('./temp/{} of {}'.format(meth, pic_name), img)
    return result


if __name__ == '__main__':
    # pp = uiautomator2.connect_usb('8DF6R16729018868')
    pp = uiautomator2.connect_usb('0071ea56')
    # print(pp.window_size())
    pp.screenshot("home.jpg")

    imsrc = cv2.imread('home.jpg')
    # img_gray = cv2.cvtColor(imsrc, cv2.COLOR_BGR2GRAY)
    img_big = imsrc.copy()
    pic_files = os.listdir('./pic')
    for pic_name in pic_files:
        im_small = cv2.imread(os.path.join('./pic', pic_name))
        methods = [ 'cv2.TM_CCOEFF_NORMED']
        # methods = ['cv2.TM_CCORR_NORMED']
        for meth in methods:
            print('Parent process %s.' % os.getpid())
            p = Process(target=match_pic, args=(img_big, im_small, meth, pic_name))
            print('Child process will start.')
            p.start()
            p.join()
            print('All subprocesses done.')


