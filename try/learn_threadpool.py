# -*-coding:utf8-*-
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time, threading, random, multiprocessing


def work(i, n):
    print(threading.current_thread().name, "-{}-{}-开始执行啦，休息{}秒\t\n".format(i, n, n), end="")
    time.sleep(n)
    print(threading.current_thread().name, "-{}-{}-执行完毕\t\n".format(i, n), end='')


def doing(thread2):
    print('休息一会{}'.format(t := random.randint(1, 5)))
    time.sleep(t)
    # for i in range(10):
    #     task = thread2.submit(work, i, random.randint(1, 5))
    #     task_list.append(task)
    #     task.running()
        # task.result()


if __name__ == '__main__':
    thread2 = ThreadPoolExecutor(max_workers=10)
    process1 = ProcessPoolExecutor(max_workers=10)
    pool = multiprocessing.Pool(30)
    task_list = []
    for j in range(100):
        pool.apply_async(doing, (thread2,))
        # task = process1.submit(doing, thread2)
        # task_list.append(task)
        # task.running()
        # task.result()
        pool.close()
        pool.join()
    print("\n线程都准备好了\t\n")
    process1.shutdown(wait=True)
    thread2.shutdown(wait=True)
    print("\t\n全部执行完毕")









