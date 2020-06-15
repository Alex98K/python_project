import cv2
import numpy as np


def PicMatchTemplate(img_big, im_small, threshold=0.8, method=cv2.TM_CCOEFF_NORMED):
    """
    图片匹配函数，基于cv2.matchTemplate，排除了重复匹配的结果，不能在某点附近多次匹配
    输入图像必须都为彩色或者灰度图片，否则报错
    :param img_big: 输入大图cv2.imread结果
    :param im_small:输入小图cv2.imread结果
    :param threshold:匹配值选择0.0-1.0
    :param method:匹配方法，默认TM_CCOEFF_NORMED，可以选TM_CCORR_NORMED
    :return:匹配到的图片的中心点坐标
    """
    img = img_big.copy()
    # method = cv2.TM_CCORR_NORMED
    t = im_small.shape
    h, w = t[0], t[1]
    res = cv2.matchTemplate(img, im_small, method)
    # print(res)
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
    # print(result)
    pp = [0, 0]
    res = []
    for p in result:
        pp = list(pp)
        pp[0] = (p[0] + w//2)
        pp[1] = (p[1] + h//2)
        pp = tuple(pp)
        res.append(pp)
    # for p in result:
    #     cv2.rectangle(img, (p[0], p[1]), (p[0] + w, p[1] + h), (0, 0, 255), 3)
    # cv2.imwrite('./temp/{} of temp.jpg'.format(str(im_small)[16:23]), img)
    return res
