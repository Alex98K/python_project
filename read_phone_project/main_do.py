from multiprocessing import Process
from phone_connect import PhoneConnect
import uiautomator2
import random
from clean_cash import CleanCash
from app_jiao_ben.qu_tou_tiao import QuTouTiao
from app_jiao_ben.dou_yin import DouYin
from app_jiao_ben.kuai_shou import KuaiShou
from app_jiao_ben.hui_tou_tiao import HuiTouTiao
from app_jiao_ben.shua_bao import ShuaBao
from app_jiao_ben.wei_shi import WeiShi
from app_jiao_ben.huo_shan import HuoShan
from app_jiao_ben.kuai_yin import KuaiYin
from app_jiao_ben.cai_dan import CaiDan
from app_jiao_ben.xiao_tang_gao import XiaoTangGao
from app_jiao_ben.qu_ling_sheng import QuLingSheng


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

    # 调用系统应用，清理缓存和垃圾
    # CleanCash(pp).main_do()
    # 清理多余占用内存的APP
    # CleanCash(pp).app_init()

    # 开始APP任务
    QuTouTiao(phone_serial, pp).recycle_main_do(test=True)
    CleanCash(pp).app_init()

    # HuiTouTiao(phone_serial, pp).recycle_main_do(test=True)
    # CleanCash(pp).app_init()

    # KuaiYin(phone_serial, pp).recycle_main_do(test=True)
    # CleanCash(pp).app_init()

    # CaiDan(phone_serial, pp).recycle_main_do(test=True)
    # CleanCash(pp).app_init()

    # XiaoTangGao(phone_serial, pp).recycle_main_do(test=True)
    # CleanCash(pp).app_init()

    # QuLingSheng(phone_serial, pp).recycle_main_do(test=True)
    # CleanCash(pp).app_init()

    # ShuaBao(phone_serial, pp).recycle_main_do(test=True)
    # CleanCash(pp).app_init()

    # WeiShi(phone_serial, pp).recycle_main_do(test=True)
    # CleanCash(pp).app_init()

    # HuoShan(phone_serial, pp).recycle_main_do(test=True)
    # CleanCash(pp).app_init()

    # DouYin(phone_serial, pp).recycle_main_do(test=True)
    # CleanCash(pp).app_init()

    # KuaiShou(phone_serial, pp).recycle_main_do(test=True)
    # CleanCash(pp).app_init()

    # 调用系统应用，清理缓存和垃圾
    CleanCash(pp).main_do()
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


