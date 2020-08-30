from multiprocessing import Process
from phone_connect import PhoneConnect
import uiautomator2
import random
from app_jiao_ben.qu_tou_tiao import QuTouTiao
from app_jiao_ben.dou_yin import DouYin
from app_jiao_ben.kuai_shou import KuaiShou
from app_jiao_ben.hui_tou_tiao import HuiTouTiao
from app_jiao_ben.shua_bao import ShuaBao
from app_jiao_ben.wei_shi import WeiShi


def main_run(phone_serial):
    pp = uiautomator2.connect_usb(phone_serial)
    pp.unlock()
    pp.screen_on()
    # 禁用USB充电
    pp.shell('dumpsys battery set usb 0')
    # 设置电池电量
    pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
    # 设置电池为非充电状态
    pp.shell('dumpsys battery set status 1')
    # 查看电池状态
    # print(pp.shell('dumpsys battery').output)
    # QuTouTiao(phone_serial, pp).recycle_main_do(test=True)
    # HuiTouTiao(phone_serial, pp).recycle_main_do(test=True)
    # ShuaBao(phone_serial, pp).recycle_main_do(test=True)
    WeiShi(phone_serial, pp).recycle_main_do(test=True)
    # DouYin(phone_serial, pp).recycle_main_do(test=True)
    # KuaiShou(phone_serial, pp).recycle_main_do(test=True)
    # 设置电池为充电状态
    # pp.shell('dumpsys battery set status 2')
    # 重置电池状态
    pp.shell('dumpsys battery reset')


if __name__ == '__main__':
    process_job_list = []
    phone_list = PhoneConnect().serials
    for serial in phone_list:
        p1 = Process(target=main_run, args=(serial,))
        p1.start()
        process_job_list.append(p1)
    for j in process_job_list:
        j.join()


