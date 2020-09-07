from multiprocessing import Process
from phone_connect import PhoneConnect
import uiautomator2
import random
import time
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
from app_jiao_ben.tian_tian_ai_qing_li import TianTianAiQingLi
from app_jiao_ben.jin_ri_tou_tiao import JinRiTouTiao
from app_jiao_ben.jing_dong import JinDong
from app_jiao_ben.mi_du import MiDu
from app_jiao_ben.xiang_kan import XiangKan


def main_run(phone_serial):
    pp = uiautomator2.connect_usb(phone_serial)
    pp.unlock()
    pp.screen_on()
    print(pp.address)

    # 测试代码部分
    # raise

    # 禁用USB充电
    pp.shell('dumpsys battery set usb 0')
    # 设置电池电量
    pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
    # 设置电池为非充电状态
    pp.shell('dumpsys battery set status 1')

    # 调用系统应用，清理缓存和垃圾
    # CleanCash(pp).main_do()
    # 清理多余占用内存的APP
    CleanCash(pp).app_init()

    # 开始APP任务
    # XiangKan(phone_serial, pp).recycle_main_do(test=True, target_coin=10000, duration=3600, cash_out=False)
    # 低收益app： 天天爱清理，米读，快音，小糖糕,
    # raise

    # 随机执行
    t = time.time()
    job_list = [i for i in range(100)]
    # random.shuffle(job_list)
    for k in job_list:
        if k == 0:
            JinDong(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 1:
            JinRiTouTiao(phone_serial, pp).recycle_main_do(target_coin=7000)
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 2:
            QuTouTiao(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 3:
            HuiTouTiao(phone_serial, pp).recycle_main_do(target_coin=7000)
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 4:
            CaiDan(phone_serial, pp).recycle_main_do(target_coin=10000)
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 5:
            QuLingSheng(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 6:
            ShuaBao(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 7:
            WeiShi(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 8:
            HuoShan(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 9:
            DouYin(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 10:
            KuaiShou(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 11:
            XiangKan(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 12:
            pass
        elif k == 13:
            pass
        elif k == 14:
            pass
        elif k == 15:
            pass
        elif k == 16:
            pass
        elif k == 17:
            pass
        elif k == 18:
            pass
        elif k == 19:
            pass
        elif k == 20:
            pass
        elif k == 21:
            MiDu(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 22:
            XiaoTangGao(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 23:
            KuaiYin(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        elif k == 24:
            TianTianAiQingLi(phone_serial, pp).recycle_main_do()
            pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
            CleanCash(pp).app_init()
            pass
        else:
            pass

        if time.time() - t > 50000:
            break

    # 调用系统应用，清理缓存和垃圾
    CleanCash(pp).main_do()
    # 重置电池状态
    pp.shell('dumpsys battery reset')
    pp.screen_off()


if __name__ == '__main__':
    process_job_list = []
    phone_list = PhoneConnect().serials
    for serial in phone_list:
        p1 = Process(target=main_run, args=(serial,))
        p1.start()
        process_job_list.append(p1)
    for j in process_job_list:
        j.join()
