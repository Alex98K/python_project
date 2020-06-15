import aircv as ac
import cv2


imsrc = ac.imread('tiao2.jpg') # 原始图像
imsch = ac.imread('qizi.jpg') # 带查找的部分


# print(ac.find_sift(imsrc, imsch))
# - when Not found
# @return None
# 之前是返回的 []
# - when found
# @return {'point': (203, 245), 'rectangle': [(160, 24), (161, 66), (270, 66), (269, 24)], 'confidence': 0.09}
# point: 查找到的点
# rectangle： 目标图像周围四个点的坐标
# SIFT查找图像
# confidence: 查找图片匹配成功的特征点 除以 总的特征点

# SIFT多个相同的部分查找
# print ac.find_all_sift(imsrc, imsch, maxcnt = 0)
# - when not found
# @return []
# - when found
# @return [{..}, {..}]
# {..}的内容跟SIFT查找到单个图像的格式一样maxcnt是可选参数，限制最多匹配的数量。


# 直接匹配查找图像
# print(ac.find_template(imsrc, imsch, threshold=0.7))
# 期望输出 (目标图片的中心点，相似度)， 相似度是电脑计算出来的一个值，跟平常所说的相似97%不是一个意思。对于这个值，达到0.999以上才算是图片一样。
# (294, 13), 0.9715

# 查找多个相同的图片，如在图形1中查找图形2
all_pos = ac.find_all_template(imsrc, imsch, threshold=0.7)
for i in all_pos:
    print(i['rectangle'])
    cv2.rectangle(imsrc, i['rectangle'][0], i['rectangle'][3], (255, 0, 0), 5)
cv2.imwrite('1.jpg', imsrc)
# cv2.imshow('haha', imsrc)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 图片拉伸
# width,height = img.shape[:2][::-1]
#     #将图片缩小便于显示观看
#     img_resize = cv2.resize(img,
#     (int(width*0.5),int(height*0.5)),interpolation=cv2.INTER_CUBIC)
#     cv2.imshow("img",img_resize)

# 二值化处理
# ret, im_fixed = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
# cv2.imwrite('gray.jpg', im_fixed)
#伽马变换
# gamma = copy.deepcopy(gray)
# rows = im_big_1.shape[0]
# cols = im_big_1.shape[1]
# for i in range(rows):
#     for j in range(cols):
#         gamma[i][j] = 3*pow(gamma[i][j], 0.8)
# cv2.imwrite('gray.jpg', gamma)

# 期望输出 (目标图片的中心点，相似度)
# [((294, 13), 0.9715), ...]

# 实例
# import aircv
#
# imsrc = aircv.Image('demo.png')
# imobj = aircv.Image('object.png')
#
# print imsrc.find(imobj, method=aircv.FIND_TMPL) # or method=aircv.FIND_SIFT
# # expect aircv.Position(x=10, y=20, extra={'method': aircv.FIND\_TMPL, 'result': 0.98})
#
# print imobj.find_in(imsrc, method=aircv.FIND_TMPL)
# # expect aircv.Position(x=10, y=20)
#
# rect = aircv.Rect(left=80, top=10, width=50, height=90)
# # Rect define: Rect(left=0, top=0, right=None, bottom=None, width='100%', height='100%')
# pos = imsrc.find(imobj, rect=rect, method=aircv.FIND_TMPL)
# print pos
# # expect aircv.Position(x=10, y=20)
# print imsrc.draw_point(pos) # .draw_point(pos2)
# # expect aircv.Image object
#
# print imsrc.draw_rectangle(aircv.Rect(left=80))
# # expect aircv.Image object
#
# print imsrc.draw_circle(??)
#
# print imsrc.cv_object
# # expect numpy object
#
# imsrc.save('source.png')
# # An Exception raised when file exists
#
# print imsrc.rect() == imobj.rect()
# # expect True or False
#
# print imsrc.percent(imobj)


# Python 实现图片加框和加字
# 第四步：设置需要画框的左上角与右下角的坐标，必须是整数
# sx1, sx2, sy1, sy2
# cv2.rectangle(imsrc,(int(sx1),int(sy1)),(int(sx2),int(sy2)),(0,255,0),3)
# 函数参数： 图片， 左上角， 右下角， 颜色， 线条粗细， 线条类型，点类型
# 第五步：加字，下例是将字加到图片上方
# if (sy1 > 10):
#     cv2.putText(im, name, (int(sx1),int(sy1-6)), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8, (0, 255, 0) )
# else:
#     cv2.putText(im, name, (int(sx1),int(sy1+15)), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8, (0, 255, 0) )
