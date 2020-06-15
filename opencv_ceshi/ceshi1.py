import cv2
from matplotlib import pyplot as plt
import numpy as np
import aircv

# img = cv2.imread('foo.png', cv2.IMREAD_UNCHANGED)
# print(img.shape, img.size)
# ball=img[280:340,330:390]
# img[273:333,100:160]=ball
# b, g, r = cv2.split(img)
# print(b ,g, r)
# cv2.imshow("haha", r)
# cv2.waitKey(0)
# cv2.imshow("he", cv2.merge((b, g, r)))
# cv2.waitKey(0)


# print(img)
# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow('image',img)
# k = cv2.waitKey(1)
# print(k)
# cv2.destroyAllWindows()
# cv2.imwrite('messigray.png',img)
#
# # img = cv2.imread('foo.png',1)
# pt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# pt.xticks([]), pt.yticks([]) # to hide tick values on X and Y axis
# pt.show()

# cap = cv2.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

# cap = cv2.VideoCapture('out.mkv')
# while True:
# # Capture frame-by-frame
#     ret, frame = cap.read()
# # Our operations on the frame come here
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# # Display the resulting frame
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()

# cap = cv2.VideoCapture(0)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
# while cap.isOpened():
#     ret, frame = cap.read()
#     if ret:
#         # 倒置摄像头图像
#         # frame = cv2.flip(frame, 0)
#         out.write(frame)
#         cv2.imshow('frame', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break
# cap.release()
# out.release()
# cv2.destroyAllWindows()

# events=[i for i in dir(cv2) if 'EVENT'in i]
# print(events)
# def draw_circle(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         cv2.circle(img, (x, y), 10, (255, 0, 0), -1)


# 创建图像与窗口并将窗口与回调函数绑定
# img = np.zeros((512, 512, 3), np.uint8)
# cv2.namedWindow('image', cv2.WINDOW_GUI_NORMAL)
# cv2.setMouseCallback('image', draw_circle)
# while(1):
#     cv2.imshow('image', img)
#     if cv2.waitKey(20) & 0xFF == 27:
#         break
# cv2.destroyAllWindows()

# def nothing(x):
#     pass
# # 创建一副黑色图像
# img=np.zeros((300,512,3),np.uint8)
# cv2.namedWindow('image')
# cv2.createTrackbar('R','image',0,255,nothing)
# cv2.createTrackbar('G','image',0,255,nothing)
# cv2.createTrackbar('B','image',0,255,nothing)
# switch='0:OFF\n1:ON'
# cv2.createTrackbar(switch,'image',0,1,nothing)
# while(1):
#     cv2.imshow('image',img)
#     k=cv2.waitKey(1)&0xFF
#     if k==27:
#         break
#     r=cv2.getTrackbarPos('R','image')
#     g=cv2.getTrackbarPos('G','image')
#     b=cv2.getTrackbarPos('B','image')
#     s=cv2.getTrackbarPos(switch,'image')
#     if s==0:
#         img[:]=0
#     else:
#         img[:]=[b,g,r]
# cv2.destroyAllWindows()

# BLUE=[255,0,0]
# img1=cv2.imread('foo.png')
# replicate = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REPLICATE)
# reflect = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REFLECT)
# reflect101 = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_REFLECT_101)
# wrap = cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_WRAP)
# constant= cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_CONSTANT,value=BLUE)
# plt.subplot(231),plt.imshow(img1,'gray'),plt.title('ORIGINAL')
# plt.subplot(232),plt.imshow(replicate,'gray'),plt.title('REPLICATE')
# plt.subplot(233),plt.imshow(reflect,'gray'),plt.title('REFLECT')
# plt.subplot(234),plt.imshow(reflect101,'gray'),plt.title('REFLECT_101')
# plt.subplot(235),plt.imshow(wrap,'gray'),plt.title('WRAP')
# plt.subplot(236),plt.imshow(constant,'gray'),plt.title('CONSTANT')
# plt.show()

# cap=cv2.VideoCapture(0)
# while True:
# # 获取每一帧
#     ret,frame=cap.read()
# # 转换到 HSV
#     hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
# # 设定蓝色的阈值
#     lower_blue=np.array([110,50,50])
#     upper_blue=np.array([130,255,255])
# # 根据阈值构建掩模
#     mask=cv2.inRange(hsv,lower_blue,upper_blue)
# # 对原图像和掩模进行位运算
#     res=cv2.bitwise_and(frame,frame,mask=mask)
# # 显示图像
#     cv2.imshow('frame',frame)
#     cv2.imshow('mask',mask)
#     cv2.imshow('res',res)
#     k=cv2.waitKey(5)&0xFF
#     if k==27:
#         break
# # 关闭窗口
# cv2.destroyAllWindows()

# img=cv2.imread('foo.png')
# # 下面的 None 本应该是输出图像的尺寸，但是因为后边我们设置了缩放因子
# # 因此这里为 None
# res=cv2.resize(img,(300,400),fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
# #OR
# # 这里呢，我们直接设置输出图像的尺寸，所以不用设置缩放因子
# # height,width=img.shape[:2]
# # res=cv2.resize(img,(2*width,2*height),interpolation=cv2.INTER_CUBIC)
# while(1):
#     cv2.imshow('res',res)
#     cv2.imshow('img',img)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
# cv2.destroyAllWindows()

# img = cv2.imread('foo.png')
# kernel = np.ones((5,5),np.float32)/25
#cv.Filter2D(src, dst, kernel, anchor=(-1, -1))
#ddepth –desired depth of the destination image;
#if it is negative, it will be the same as src.depth();
#the following combinations of src.depth() and ddepth are supported:
#src.depth() = CV_8U, ddepth = -1/CV_16S/CV_32F/CV_64F
#src.depth() = CV_16U/CV_16S, ddepth = -1/CV_32F/CV_64F
#src.depth() = CV_32F, ddepth = -1/CV_32F/CV_64F
#src.depth() = CV_64F, ddepth = -1/CV_64F
#when ddepth=-1, the output image will have the same depth as the source.
# dst = cv2.filter2D(img,-1,kernel)
# plt.subplot(121),plt.imshow(img),plt.title('Original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(dst),plt.title('Averaging')
# plt.xticks([]), plt.yticks([])
# plt.show()

# img = cv2.imread('foo.png',0)
# edges = cv2.Canny(img,100,200)
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()

# img = cv2.imread('temp_all.jpg')
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray,50,150,apertureSize = 3)
# lines = cv2.HoughLines(edges,1,np.pi/180,200)
# for rho,theta in lines[0]:
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))
#     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
# cv2.imwrite('houghlines3.jpg',img)

# filename = 'temp_all.jpg'
# img = cv2.imread(filename)
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# gray = np.float32(gray)
# # 输入图像必须是 float32，最后一个参数在 0.04 到 0.05 之间
# dst = cv2.cornerHarris(gray,2,3,0.04)
# #result is dilated for marking the corners, not important
# dst = cv2.dilate(dst,None)
# # Threshold for an optimal value, it may vary depending on the image.
# img[dst>0.01*dst.max()]=[0,0,255]
# cv2.imshow('dst',img)
# if cv2.waitKey(0) & 0xff == 27:
#     cv2.destroyAllWindows()

# img = cv2.imread('tiao2.jpg')
# gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# sift = cv2.xfeatures2d.SIFT_create()
# kp = sift.detect(gray,None)
# img=cv2.drawKeypoints(gray,kp,img)
# cv2.namedWindow("haha", cv2.WINDOW_KEEPRATIO)
# cv2.imshow('haha',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# img1 = cv2.imread('tiao2.jpg',0) # queryImage
# img2 = cv2.imread('red.jpg',0) # trainImage
# # Initiate SIFT detector
# orb = cv2.ORB()
# # find the keypoints and descriptors with SIFT
# kp1, des1 = orb.detectAndCompute(img1,None)
# kp2, des2 = orb.detectAndCompute(img2,None)
# # create BFMatcher object
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# # Match descriptors.
# matches = bf.match(des1,des2)
# # Sort them in the order of their distance.
# matches = sorted(matches, key = lambda x:x.distance)


# img = cv2.imread('tiao3.jpg')
# mask = cv2.imread('tiao2.png')
# dst = cv2.inpaint(img,mask,3,cv2.INPAINT_TELEA)


# print(img.item(100,200,1))
# img[300:400, 100:200, :], img[400:500, 200:300, :] = img[400:500, 200:300, :], img[300:400, 100:200, :]
# cv2.namedWindow("hah", cv2.WINDOW_KEEPRATIO)
# cv2.imshow('hah',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# sift=cv2.xfeatures2d.SIFT_create()#创建sift检测器

# orb = cv2.ORB_create()
# kp1,des1 = orb.detectAndCompute(img,None)
# kp2,des2 = orb.detectAndCompute(mask,None) #计算img2中的
# bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True) #建立匹配关系
# mathces=bf.match(des1, des2) #匹配描述符
# mathces=sorted(mathces,key=lambda x:x.distance) #据距离来排序
# img3 = cv2.drawMatches(img,kp1,mask,kp2,mathces[:40]) #画出匹配关系
# plt.imshow(img3)
# plt.show() #matplotlib描绘出来

img = cv2.imread("temp_all.jpg", 1)
print(img.shape)
height = img.shape[0]
width = img.shape[1]
dst_height = height//2
dst_width = width//2
dst = cv2.resize(img, (dst_width, dst_height))
# dst1 = dst[100:200, 300:500]
matshift = np.float32([[1,0,100],[0,1,200]])
dst1 = cv2.warpAffine(dst, matshift,(dst_height,dst_width))
cv2.imshow('heh', dst1)
cv2.waitKey(0)
# cv2.imwrite('1.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 50])
# cv2.imwrite('1.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 7])

# data1 = np.array([1,2,3,4,5])
# print(data1)
# data2 = np.array([[1,2],
#                  [3,4]])
# print(data2)
# print(data1.shape, data2.shape)
# print(np.zeros([2,4]),np.ones([3,3]))
# data2[1,0] = 10
# print(data2)
# data3 = np.ones([2,3])
# print(data3*3)
# print(data3+3)
# data4 = np.array([[2,3,4],[5,6,7]])
# print(data3*2*data4)





