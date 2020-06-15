import win32con
import win32gui
import win32api

wind = win32gui.FindWindow(0, 'xiaoxiaole')
handleDetail = win32gui.GetWindowRect(wind)
#获取某个句柄的类名和标题
title = win32gui.GetWindowText(wind)
clsname = win32gui.GetClassName(wind)
subHandle = win32gui.FindWindowEx(0, 0, 0, "如何利用Python和win32编程避免重复性体力劳动（一）——开始、FindWindow和FindWindowEx - 游走的psychiatrist - CSDN博客")
print(wind,handleDetail,title,clsname,subHandle)
win32api.MessageBox(0,"Hello PYwin32","MessageBox",win32con.MB_OK | win32con.MB_ICONWARNING)

COL_NUM = 19
ROW_NUM = 11
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)
hwnd = win32gui.FindWindow(win32con.NULL, 'xiaoxiaole')
if hwnd == 0:
    exit('没有找到窗口')

# 显示窗口
# SW_HIDE：隐藏窗口并激活其他窗口。nCmdShow=0。
# SW_MAXIMIZE：最大化指定的窗口。nCmdShow=3。
# SW_MINIMIZE：最小化指定的窗口并且激活在Z序中的下一个顶层窗口。nCmdShow=6。
# SW_RESTORE：激活并显示窗口。如果窗口最小化或最大化，则系统将窗口恢复到原来的尺寸和位置。在恢复最小化窗口时，应用程序应该指定这个标志。nCmdShow=9。
# SW_SHOW：在窗口原来的位置以原来的尺寸激活和显示窗口。nCmdShow=5。
# SW_SHOWDEFAULT：依据在STARTUPINFO结构中指定的SW_FLAG标志设定显示状态，STARTUPINFO 结构是由启动应用程序的程序传递给CreateProcess函数的。nCmdShow=10。
# SW_SHOWMAXIMIZED：激活窗口并将其最大化。nCmdShow=3。
# SW_SHOWMINIMIZED：激活窗口并将其最小化。nCmdShow=2。
# SW_SHOWMINNOACTIVE：窗口最小化，激活窗口仍然维持激活状态。nCmdShow=7。
# SW_SHOWNA：以窗口原来的状态显示窗口。激活窗口仍然维持激活状态。nCmdShow=8。
# SW_SHOWNOACTIVATE：以窗口最近一次的大小和状态显示窗口。激活窗口仍然维持激活状态。nCmdShow=4。
# SW_SHOWNORMAL：激活并显示一个窗口。如果窗口被最小化或最大化，系统将其恢复到原来的尺寸和大小。应用程序在第一次显示窗口的时候应该指定此标志。nCmdShow=1。
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
# 函数将创建指定的窗口，并激活到前台窗口的线程 。键盘输入窗口，并为用户更改不同的视觉线索。该系统分配一个优先略高前景的窗口，比它其他线程创建的线程。
win32gui.SetForegroundWindow(hwnd)
# 返回窗口左上右下坐标
window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
if min(window_left, window_top) < 0 or window_right > screen_width or window_bottom > screen_height:
    exit('haha')
window_width = window_right - window_left
window_height = window_bottom - window_top