import aircv as ac
import cv2
import uiautomator2
# from PIL import Image
import core
import copy
import time


class ShuduAuto(object):
    def __init__(self):
        # self.pp = uiautomator2.connect_usb('8DF6R16729018868')
        self.pp = uiautomator2.connect_usb('0071ea56')
        # self.pp = uiautomator2.connect_wifi('192.168.1.218')
        # 打印屏幕分辨率
        print("屏幕分辨率是", self.pp.window_size())
        # 打印窗口组件的结构
        # print(self.pp.dump_hierarchy())

    def get_num_pic(self):
        # 截取游戏主屏幕的图片，返回图片读取文件
        self.pp.screenshot("temp_all.jpg")
        self.im_all = ac.imread('temp_all.jpg')

    def vertex_position(self):
        # 计算数独数组所在大框的左上和右下角的坐标
        im_ver = ac.imread('./pic/pad/ver.jpg')
        im_lat = ac.imread('./pic/pad/lat.jpg')
        lef_up_x = lef_up_y = right_down_x = right_down_y = 0
        all_pos_ver = ac.find_all_template(self.im_all, im_ver, threshold=0.9)
        for i in all_pos_ver:
            # print(i['rectangle'])
            lef_up_x = i['rectangle'][0][0]
            right_down_x = i['rectangle'][3][0]
        all_pos_lat = ac.find_all_template(self.im_all, im_lat, threshold=0.9)
        for i in all_pos_lat:
            # print(i['rectangle'])
            lef_up_y = i['rectangle'][0][1]
            right_down_y = i['rectangle'][3][1]
        if lef_up_y and lef_up_x and right_down_y and right_down_x:
            x1_y1 = (lef_up_x, lef_up_y)
            x2_y2 = (right_down_x, right_down_y)
        else:
            print("没有获取左上角和右下角坐标")
            print(lef_up_x, lef_up_y, right_down_x, right_down_y)
            raise
        return x1_y1, x2_y2

    def shudu_big_position(self):
        # 数独数字所在小方格的左上和右下角的坐标序列
        x1_y1, x2_y2 = self.vertex_position()
        # print(x1_y1, x2_y2)
        # 9*9 数独数字所在表格各小方格的横竖轴坐标
        x_lab = [i for i in range(x1_y1[0], x2_y2[0], (x2_y2[0]-x1_y1[0])//9)]
        y_lab = [i for i in range(x1_y1[1], x2_y2[1], (x2_y2[1]-x1_y1[1])//9)]
        # print(x_lab, y_lab)
        return x_lab, y_lab

    def shudu_every_cube(self, x_lab, y_lab):
        # 生成9*9数独数据框中每个方格的中心点点击坐标
        num_press_center = [[0 for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                num_press_center[i][j] = ((x_lab[j]+x_lab[j+1])//2, (y_lab[i]+y_lab[i+1])//2)
        # print("num_press_center", num_press_center)
        return num_press_center

    def shudu_list(self, x_lab, y_lab):
        # 生成数独数字的二维数组
        # 初始化9*9空数组,每个为0
        num_list_orn = [[0 for i in range(9)] for j in range(9)]
        for i in range(1, 10):
            img_name = ac.imread('./pic/pad/num_{}.jpg'.format(str(i)))
            all_pos_num = ac.find_all_template(self.im_all, img_name, threshold=0.9)
            for p in all_pos_num:
                # print(p)
                for j in range(10):
                    if int(p['result'][0]) < x_lab[j]:
                        i_y = j-1
                        break
                for k in range(10):
                    if int(p['result'][1]) < y_lab[k]:
                        i_x = k-1
                        break
                # print(i_x, i_y)
                num_list_orn[i_x][i_y] = i
        return num_list_orn

    def shudu_num_position(self, num_list_orn, num_press_center):
        # num_list_orn是用来点击空格的
        # 生成下面的要点击输入的1-9数字的坐标列表,首先点击没有数字的空格，出现下面输入数字的框
        break_logo = i_x = i_y = 0
        for i in range(9):
            for j in range(9):
                if num_list_orn[i][j] == 0:
                    i_x = i
                    i_y = j
                    break_logo = 1
                    break
            if break_logo == 1:
                break
        self.pp.click(num_press_center[i_x][i_y][0], num_press_center[i_x][i_y][1])
        self.pp.screenshot("temp_all_num.jpg")
        im_all_num = ac.imread('temp_all_num.jpg')
        # 获取坐标
        press_num_input = []
        for i in range(1, 10):
            img_name = ac.imread('./pic/pad/input_{}.jpg'.format(str(i)))
            pos_num = ac.find_template(im_all_num, img_name, threshold=0.8)
            try:
                press_num_input.append(pos_num['result'])
            except Exception as e:
                print('没有获取到下面输入数字{}的坐标匹配图'.format(i))
                raise
        if not press_num_input:
            print("下面输入数字窗口的中心点坐标数组有误")
            raise
        else:
            return press_num_input

    def press_input_shudu(self, num_press_center, press_num_input, num_list_result):
        # 输入数独结果数字的操作函数
        # 开始输入数字
        for i in range(9):
            for j in range(9):
                if self.num_list_orn[i][j] == 0:
                    num = num_list_result[i][j]
                    self.pp.click(num_press_center[i][j][0], num_press_center[i][j][1])
                    self.pp.click(press_num_input[num - 1][0], press_num_input[num - 1][1])

    def run_return_num(self):
        # 启动函数，将屏幕中数独的数字打入二维数组
        self.get_num_pic()
        self.x_lab, self.y_lab= self.shudu_big_position()
        self.shudu_every_cube(self.x_lab, self.y_lab)
        self.num_list_orn = self.shudu_list(self.x_lab, self.y_lab)
        # print(self.num_list_orn)
        return self.num_list_orn

    def run_input_num(self, num_list_result):
        # 启动函数，按照输入的计算出的数独结果，在屏幕中录入数字
        num_press_center = self.shudu_every_cube(self.x_lab, self.y_lab)
        press_num_input = self.shudu_num_position(self.num_list_orn, num_press_center)
        self.press_input_shudu(num_press_center, press_num_input, num_list_result)

    def main(self):
        # 单独过一关的主函数
        num_list = copy.deepcopy(shudu.run_return_num())
        # 数独算法，从原始num_list_orn，计算出结果num_list_result
        num_list_result = core.main(num_list)
        shudu.run_input_num(num_list_result)

    def continue_past(self):
        # 连续过关的主函数
        while True:
            self.pp.screenshot("temp_all_next.jpg")
            im_all_next = ac.imread('temp_all_next.jpg')
            img_next = ac.imread('./pic/pad/next.jpg')
            pos_num = ac.find_template(im_all_next, img_next, threshold=0.8)
            if pos_num:
                # print(pos_num)
                self.pp.click(int(pos_num['result'][0]), int(pos_num['result'][1]))
            time.sleep(0.5)
            self.main()


if __name__ == '__main__':
    shudu = ShuduAuto()
    shudu.continue_past()