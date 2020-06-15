import pyautogui as pag
import PIL
import cv2
import aircv


screenWidth, screenHeight = pag.size()
print(screenWidth, screenHeight)
#  返回一个Pillow/PIL的Image对象
img=pag.screenshot()
img.save('foo.png')
pag.screenshot('foo.png')

(r,g,b)=img.getpixel((50, 201))
print((r,g,b))
# (30, 132, 153)

#  当前鼠标的坐标
# pyautogui.position()
#  当前屏幕的分辨率（宽度和高度）
# pyautogui.size
#  (x,y)是否在屏幕上
# x, y = 122, 244
# pyautogui.onScreen(x, y)

#  返回(最左x坐标，最顶y坐标，宽度，高度)
# pyautogui.locateOnScreen('pyautogui/looks.png')
# locateAllOnScreen()函数会寻找所有相似图片，返回一个生成器：
# for i in pyautogui.locateAllOnScreen('pyautogui/looks.png'):
#     print(i)
# list(pyautogui.locateAllOnScreen('pyautogui/looks.png'))
# locateCenterOnScreen()函数会返回图片在屏幕上的中心XY轴坐标值：
# pyautogui.locateCenterOnScreen('pyautogui/looks.png')
# 定位比较慢，一般得用1~2秒

# 判断屏幕坐标的像素是不是等于某个值
ifEqual=pag.pixelMatchesColor(50, 200, (30, 132, 153))
print(ifEqual)
#True

# 区域截图
img = pag.screenshot(region=(0, 0, 300 ,400))
img.save('1.jpg')

currentMouseX, currentMouseY = pag.position()
print(currentMouseX, currentMouseY)
# pag.click()

# pag.click(x=300, y=500, button='right')
# x，y是要点击的位置，默认是鼠标当前位置 button是要点击的按键，有三个可选值：‘left’, ‘middle’, ‘right’

# pag.mouseDown(x=moveToX, y=moveToY, button='left')
# pag.mouseUp(x=moveToX, y=moveToY, button='left')

# pag.doubleClick()
# pag.rightClick()
# pag.middleClick()
# 鼠标移动
# pag.moveTo(x,y,duration) #  绝对坐标
# pag.moveRel(x,y,duration) # 相对坐标
# 鼠标拖拽
# pag.dragTo(x,y,duration)
# pag.dragRel(x,y,duration)

# 多次点击
# 可以设置clicks参数，还有interval参数可以设置每次单击之间的时间间隔。例如：
#  双击左键
# pag.click(clicks=2)
#  两次单击之间停留0.25秒
# pag.click(clicks=2, interval=0.25)
#  三击右键
# pag.click(button='right', clicks=2, interval=0.25)
# 滚轮
# 使用函数scroll()，它只接受一个整数。如果值为正往上滚，值为负往下滚。
# pag.scroll(200)


# 键盘操作
# 输入字符串
# pag.typewrite('Hello world')
# 上面的字符串是一次输入，为了唬人可以延迟输入
# pag.typewrite('Hello world!', 0.1)
# Hello worldHello world!Hello worldHello world!Hello world!Hello world!Hello world!Hello world!

# pag.keyDown() # 按下某个键
# pag.keyUp() # 松开某个键
# pag.press('f1') # 一次完整的击键，前面两个函数的组合。
# pag.hotkey('ctrl', 'c') # 热键函数

pag.alert('这个消息弹窗是文字+OK按钮')
pag.confirm('这个消息弹窗是文字+OK+Cancel按钮')
rs = pag.prompt('这个消息弹窗是让用户输入字符串，单击OK')
rt = pag.password('这个消息弹窗是让用户输入字符串，单击OK')
#返回用户输入的字符串，如果用户什么都不输入，则返回None
print(rs, rt)

# 通过把pyautogui.PAUSE设置成float或int时间（秒），可以为所有的PyAutoGUI函数增加延迟。
# 默认延迟时间是0.1秒。在函数循环执行的时候，这样做可以让PyAutoGUI运行的慢一点，非常有用。例如：
# pag.PAUSE = 2.5
# pag.moveTo(100,100);
# pag.click()


