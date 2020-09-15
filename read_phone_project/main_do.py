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
from app_jiao_ben.dong_fang_tou_tiao import DongFangTouTiao
from app_jiao_ben.shan_dian_he_zi import ShanDianHezi
from app_jiao_ben.wei_li_kan_kan import WeiLiKanKan
from app_jiao_ben.hong_bao_shi_pin import HongBaoShiPin
from app_jiao_ben.sou_hu_zi_xun import SouHuZiXun
from app_jiao_ben.mo_fang_kan_dian import MoFangKanDian


def main_run(phone_serial):
    """ 用来测试的乐视X620手机序列号是    LE67A06150003303   """
    pp = uiautomator2.connect_usb(phone_serial)
    time.sleep(1)
    pp.unlock()
    time.sleep(1)
    pp.screen_on()
    print(pp.address)

    # 测试代码部分
    # 重置电池状态
    # pp.shell('dumpsys battery reset')
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
    # CleanCash(pp).app_init()

    # 低收益app： 天天爱清理，米读，快音，小糖糕, 彩蛋，趣铃声
    # 大部分APP都是前面刷的快，后面慢

    # 程序开始运行，开始APP任务
    t = time.time()
    job_list = [i for i in range(100)]
    # 随机执行
    # random.shuffle(job_list)
    for k in job_list:
        if k == -1:
            continue
        # elif k == 0:
        #     JinDong(phone_serial, pp).recycle_main_do(target_coin=5000)
        # elif k == 1:
        #     JinRiTouTiao(phone_serial, pp).recycle_main_do(target_coin=6500)
        # elif k == 2:
        #     QuTouTiao(phone_serial, pp).recycle_main_do(target_coin=7000)
        # elif k == 3:
        #     HuiTouTiao(phone_serial, pp).recycle_main_do(target_coin=5000)
        # elif k == 4:
        #     CaiDan(phone_serial, pp).recycle_main_do(target_coin=3000)
        # elif k == 5:
        #     QuLingSheng(phone_serial, pp).recycle_main_do(target_coin=2000)
        # elif k == 6:
        #     ShuaBao(phone_serial, pp).recycle_main_do(target_coin=6000)
        # elif k == 7:
        #     # 这个APP特别卡，没有今日金币获取地方，在看视频过程中还有滑块验证
        #     WeiShi(phone_serial, pp).recycle_main_do(target_coin=1000)
        # elif k == 8:
        #     HuoShan(phone_serial, pp).recycle_main_do(target_coin=3000)
        # elif k == 9:
        #     DouYin(phone_serial, pp).recycle_main_do(target_coin=2000)
        # elif k == 10:
        #     KuaiShou(phone_serial, pp).recycle_main_do(target_coin=6000)
        # elif k == 11:
        #     XiangKan(phone_serial, pp).recycle_main_do(target_coin=1000)
        # elif k == 12:
        #     MiDu(phone_serial, pp).recycle_main_do(target_coin=1000)
        # elif k == 13:
        #     XiaoTangGao(phone_serial, pp).recycle_main_do(target_coin=2000)
        # elif k == 14:
        #     KuaiYin(phone_serial, pp).recycle_main_do(target_coin=2000)
        # elif k == 15:
        #     TianTianAiQingLi(phone_serial, pp).recycle_main_do(target_coin=2000)
        # elif k == 16:
            # 这个注册时候账号异常，客服说不影响使用，但是被系统检测到了，尝试了下，可以获得金币，提现还在测试
            # ShanDianHezi(phone_serial, pp).recycle_main_do(target_coin=80000)
        # elif k == 17:
        #     WeiLiKanKan(phone_serial, pp).recycle_main_do(target_coin=2000)
        # elif k == 18:
        #     HongBaoShiPin(phone_serial, pp).recycle_main_do(target_coin=7000)
        # elif k == 19:
            # 这个收益太低，10万换1元
            # SouHuZiXun(phone_serial, pp).recycle_main_do(target_coin=70000)
        elif k == 20:
            MoFangKanDian(phone_serial, pp).recycle_main_do(target_coin=4000)
        else:
            continue

        pp.shell(f'dumpsys battery set level {random.randint(15, 95)}')
        CleanCash(pp).app_init()
        if time.time() - t > 50000:
            break

    # 调用系统应用，清理缓存和垃圾
    CleanCash(pp).main_do()
    # 重置电池状态
    pp.shell('dumpsys battery reset')
    # pp.screen_off()


if __name__ == '__main__':
    process_job_list = []
    phone_list = PhoneConnect().serials
    for serial in phone_list:
        p1 = Process(target=main_run, args=(serial,))
        p1.start()
        process_job_list.append(p1)
    for j in process_job_list:
        j.join()
