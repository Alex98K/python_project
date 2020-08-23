from multiprocessing import Process
from phone_connect import PhoneConnect
from app_jiao_ben.qu_tou_tiao import QuTouTiao
import uiautomator2


def main_run(key):
    QuTouTiao(key, uiautomator2.connect_usb(key)).main_do()


if __name__ == '__main__':
    process_job_list = []
    phone_list = PhoneConnect().serials
    for serial in phone_list:
        p1 = Process(target=main_run, args=(serial,))
        p1.start()
        process_job_list.append(p1)
    for j in process_job_list:
        j.join()


