import win32con
import win32gui
import win32api
import win32ui

_VK_CODE = {
    'backspace': 0x08, 'tab': 0x09, 'clear': 0x0C, 'enter': 0x0D, 'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12,
    'pause': 0x13, 'caps_lock': 0x14, 'esc': 0x1B, 'spacebar': 0x20, 'page_up': 0x21, 'page_down': 0x22,
    'end': 0x23, 'home': 0x24, 'left_arrow': 0x25, 'up_arrow': 0x26, 'right_arrow': 0x27, 'down_arrow': 0x28,
    'select': 0x29, 'print': 0x2A, 'execute': 0x2B, 'print_screen': 0x2C, 'ins': 0x2D, 'del': 0x2E, 'help': 0x2F,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45, 'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
    'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F, 'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
    'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A, 'numpad_0': 0x60, 'numpad_1': 0x61,
    'numpad_2': 0x62, 'numpad_3': 0x63, 'numpad_4': 0x64, 'numpad_5': 0x65, 'numpad_6': 0x66, 'numpad_7': 0x67,
    'numpad_8': 0x68, 'numpad_9': 0x69, 'multiply_key': 0x6A, 'add_key': 0x6B, 'separator_key': 0x6C,
    'subtract_key': 0x6D, 'decimal_key': 0x6E, 'divide_key': 0x6F, 'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73,
    'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B, 'F13': 0x7C,
    'F14': 0x7D, 'F15': 0x7E, 'F16': 0x7F, 'F17': 0x80, 'F18': 0x81, 'F19': 0x82, 'F20': 0x83, 'F21': 0x84, 'F22': 0x85,
    'F23': 0x86, 'F24': 0x87, 'num_lock': 0x90, 'scroll_lock': 0x91, 'left_shift': 0xA0, 'right_shift ': 0xA1,
    'left_control': 0xA2, 'right_control': 0xA3, 'left_menu': 0xA4, 'right_menu': 0xA5, 'browser_back': 0xA6,
    'browser_forward': 0xA7, 'browser_refresh': 0xA8, 'browser_stop': 0xA9, 'browser_search': 0xAA,
    'browser_favorites': 0xAB, 'browser_start_and_home': 0xAC, 'volume_mute': 0xAD, 'volume_Down': 0xAE,
    'volume_up': 0xAF, 'next_track': 0xB0, 'previous_track': 0xB1, 'stop_media': 0xB2, 'play/pause_media': 0xB3,
    'start_mail': 0xB4, 'select_media': 0xB5, 'start_application_1': 0xB6, 'start_application_2': 0xB7,
    'attn_key': 0xF6, 'crsel_key': 0xF7, 'exsel_key': 0xF8, 'play_key': 0xFA, 'zoom_key': 0xFB, 'clear_key': 0xFE,
    '+': 0xBB, ',': 0xBC, '-': 0xBD, '.': 0xBE, '/': 0xBF, '`': 0xC0, ';': 0xBA, '[': 0xDB, '\\': 0xDC, ']': 0xDD,
    "'": 0xDE, '`': 0xC0
    }


def screenshot(region=(0, 0, 0, 0), savepath=''):
    """
    屏幕截图，默认保存本文件夹下screenshot.bmp
    :param region:截图选择位置，左上角和右下角坐标
    :param savepath:保存路径和文件名字符串
    :return:
    """
    # 获取桌面
    hdesktop = win32gui.GetDesktopWindow()
    # 分辨率适应
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    # 创建设备描述表
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    # 创建一个内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()
    # 创建位图对象
    screenshot = win32ui.CreateBitmap()
    if region != (0, 0, 0, 0):
        # 负数是因为start_point中坐标为负，mem_dc.BitBlt才能正确截图，设定起始点偏移量
        start_point = (-region[0], -region[1])
        end_point = (region[2], region[3])
        screenshot.CreateCompatibleBitmap(img_dc, region[2] - region[0], region[3] - region[1])
    else:
        start_point = (0, 0)
        end_point = (width, height)
        screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    # 截图至内存设备描述表
    mem_dc.BitBlt(start_point, end_point, img_dc, (0, 0), win32con.SRCCOPY)
    # 将截图保存到文件中
    if not savepath:
        screenshot.SaveBitmapFile(mem_dc, 'screenshot.bmp')
    else:
        screenshot.SaveBitmapFile(mem_dc, '{}.bmp'.format(str(savepath)))
    # 内存释放
    img_dc.DeleteDC()
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())


def windowscreenshot(windtitle, region=(0, 0, 0, 0), savepath=''):
    """    窗口截图，支持后台窗口截图，但不能是最小化的窗口，
    默认保存本文件夹下windowscreenshot.bmp
    :param windtitle: 窗口句柄
    :param region: 窗口截图选择位置，左上角和右下角坐标
    :param savepath: 保存路径和文件名字符串
    :return:
    """
    # 获取要截取窗口的句柄
    hwnd = win32gui.FindWindow(0, str(windtitle))
    # 获取句柄窗口的大小信息
    # 可以通过修改该位置实现自定义大小截图
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    if right < 0 or bot < 0:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    # print(left, top, right, bot)
    # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 创建设备描述表
    img_dc = win32ui.CreateDCFromHandle(hwndDC)
    # 创建内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()
    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    if region != (0, 0, 0, 0):
        # 负数是因为start_point中坐标为负，mem_dc.BitBlt才能正确截图，设定起始点偏移量
        start_point = (-region[0], -region[1])
        end_point = (region[2], region[3])
        saveBitMap.CreateCompatibleBitmap(img_dc, region[2] - region[0], region[3] - region[1])
    else:
        start_point = (0, 0)
        end_point = (width, height)
        saveBitMap.CreateCompatibleBitmap(img_dc, width, height)
    # 将截图保存到saveBitMap中
    mem_dc.SelectObject(saveBitMap)
    # 截图至内存设备描述表
    mem_dc.BitBlt(start_point, end_point, img_dc, (0, 0), win32con.SRCCOPY)
    # 将截图保存到文件中
    if not savepath:
        saveBitMap.SaveBitmapFile(mem_dc, 'windowscreenshot.bmp')
    else:
        saveBitMap.SaveBitmapFile(mem_dc, '{}.bmp'.format(str(savepath)))
    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    img_dc.DeleteDC()
    mem_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)


def mouseclick(x=0, y=0, math='left'):
    """
    模拟鼠标单击，
    :param x: x坐标
    :param y: y坐标
    :param math: 左键，右键，中键
    :return:
    """
    math = str(math)
    if x != 0 or y != 0:
        x, y = x, y
        win32api.SetCursorPos((x, y))
    if math == 'left':
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN + win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    elif math == 'middle':
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN + win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
    elif math == 'right':
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN + win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    else:
        raise 'math input error {}'.format(math)


def mousedoubleclick(x=0, y=0, math='left'):
    """
    模拟鼠标双击，可以左键，右键，中键
    """
    math = str(math)
    if x != 0 or y != 0:
        x, y = x, y
        win32api.SetCursorPos((x, y))
    if math == 'left':
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN + win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN + win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    elif math == 'middle':
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN + win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN + win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
    elif math == 'right':
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN + win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN + win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    else:
        raise 'math input error {}'.format(math)


def mousemove(x=0, y=0):
    """
    模拟鼠标移动
    """
    win32api.SetCursorPos((x, y))


def inputstring(string=''):
    """
    模拟键盘输入字符串，输入参数为字符串
    """
    string = str(string)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN + win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    for c in string:
        win32api.keybd_event(_VK_CODE[c], 0, 0, 0)
        win32api.keybd_event(_VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)


def inputkey(string=''):
    """
    键盘模拟输入，输入特殊按键组合，例如alt，f1.输入可以是单个按键名，
    也可以是组合键的列表，比如['alt','s']
    """
    if not isinstance(string, list):
        string = str(string)
        win32api.keybd_event(_VK_CODE[string], 0, 0, 0)
        win32api.keybd_event(_VK_CODE[string], 0, win32con.KEYEVENTF_KEYUP, 0)
    elif isinstance(string, list):
        for i in string:
            win32api.keybd_event(_VK_CODE[str(i)], 0, 0, 0)
        for j in string[::-1]:
            win32api.keybd_event(_VK_CODE[str(j)], 0, win32con.KEYEVENTF_KEYUP, 0)


def mousedrag(pos=(0, 0, 0, 0), math='left'):
    """
    鼠标拖动函数，输入参数为pos，起点坐标和终点坐标的位置
    """
    math = str(math)
    if pos != (0, 0, 0, 0) and isinstance(pos, tuple):
        x1, y1, x2, y2 = pos
    else:
        raise 'pos {} error'.format(pos)
    if math == 'left':
        win32api.SetCursorPos((x1, y1))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.SetCursorPos((x2, y2))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    elif math == 'middle':
        win32api.SetCursorPos((x1, y1))
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
        win32api.SetCursorPos((x2, y2))
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
    elif math == 'right':
        win32api.SetCursorPos((x1, y1))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.SetCursorPos((x2, y2))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    else:
        raise 'math input error {}'.format(math)


def windowposition(windtitle):
    """
    输入窗口的标题，返回窗口的位置，返回四个值分别为左上角和右下角的位置坐标
    """
    hwnd = win32gui.FindWindow(0, str(windtitle))
    # 返回窗口左上右下坐标
    window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
    if window_right < 0 or window_bottom < 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
        window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
    return window_left, window_top, window_right, window_bottom


def windowall():
    """
    返回当前系统内全部窗口信息列表,每个元素的第一个是窗口句柄，
    第二个是标题，第三个是窗口类，第四个是窗口位置，如果为空，就为空白字符串
    """
    hWndList = []
    hWndresult = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    for wind in hWndList:
        try:
            handleDetail = win32gui.GetWindowRect(wind)
        except Exception:
            handleDetail = None
        try:
            title = win32gui.GetWindowText(wind)
        except Exception:
            title = None
        try:
            clsname = win32gui.GetClassName(wind)
        except Exception:
            clsname = None
        hWndresult.append((wind, title, clsname, handleDetail))
        hWndChildList = []
        try:
            win32gui.EnumChildWindows(wind, lambda hWnd, param: param.append(hWnd), hWndChildList)
        except Exception:
            pass
        for hWnd in hWndChildList:
            try:
                childtitle = win32gui.GetWindowText(hWnd)
            except Exception:
                childtitle = None
            try:
                childhandleDetail = win32gui.GetWindowRect(hWnd)
            except Exception:
                childhandleDetail = None
            try:
                childclsname = win32gui.GetClassName(hWnd)
            except Exception:
                childclsname = None
            hWndresult.append((hWnd, childtitle, childclsname, childhandleDetail))
    return hWndresult


if __name__ == '__main__':
    # screenshot(region=(376,258,1073,445))
    # screenshot()
    # windowscreenshot('梦幻西游 ONLINE - (江苏2区[枫桥夜泊] - 莫小翼[42573143])')
    # windowscreenshot('无标题 - 记事本',region=(0,0,1073,445))
    # mouseclick(x=100, y=100,math='right')
    # mousemove(x=100, y=100)
    # inputstring(123)
    # inputkey(['end','home'])
    # mousedoubleclick(x=100, y=100)
    pass


