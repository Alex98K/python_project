import logging
import sys
import pathlib
import json
import random
import time


class AppReadBase(object):
    def __init__(self, phone_serial, pp):
        self.pp = pp
        self.phone_serial = phone_serial
        self.probability_read_issue = 0.7  # 看视频或文章概率
        self.probability_scroll_up = 0.15  # 看视频或文章向上滑动（回看）的概率
        self.probability_thumb_up = 0.1  # 点赞概率
        self.probability_commit = 0.03  # 评论概率
        self.probability_focus = 0.02  # 关注概率
        self.path = pathlib.Path().cwd()
        self.logger = self.log_config(phone_serial)
        with open(self.path / 'conf' / 'app_info.json', 'r', encoding='UTF-8') as f:
            self.app_info = json.load(f)
        with open(self.path / 'conf' / 'commit.json', 'r', encoding='UTF-8') as f:
            self.commit = json.load(f)
        self.package_name = ''

    def app_start(self, app_name):
        app_list_running = self.pp.app_list_running()
        for k, v in self.app_info.items():
            if v[1] == app_name:
                self.package_name = k
                if k in app_list_running:
                    self.pp.app_stop(k)
                self.pp.app_start(k)
                self.logger.info(f'********开始 {app_name} 的任务********')
                return
        self.logger.error('app名字输入错误，无法启动app')
        raise

    def app_end(self):
        self.pp.app_stop(self.package_name)
        self.logger.info(f'********结束 APP 任务********')

    def log_config(self, phone_serial):
        # 设置log
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.DEBUG)
        # StreamHandler 输出到控制台的logger
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level=logging.INFO)
        logger.addHandler(stream_handler)
        # FileHandler 输出到文件的logger
        if not pathlib.Path(self.path / 'log').exists():
            pathlib.Path.mkdir(self.path / 'log')
        file_handler = logging.FileHandler(self.path / 'log' / f'{phone_serial}_log.txt', mode='a', encoding='UTF-8')
        file_handler.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def click_random_position(self, xpath_bounds):
        lx, ly, rx, ry = xpath_bounds
        x_off, y_off = random.random(), random.random()
        width, height = rx - lx, ry - ly
        x = lx + width * x_off
        y = ly + height * y_off
        self.pp.click(x, y)
        return x, y

    def input_num(self, num):
        self.pp.set_fastinput_ime(False)
        for j in num:
            self.pp(description=j).click(offset=(random.random(), random.random()))

    def main_do(self, duration, target_coin):
        pass

    def del_watcher(self):
        try:
            self.pp.watcher.stop()
            self.pp.watcher.remove()
        except AttributeError:
            self.logger.error('程序结束调用del注销watcher出错')

    def recycle_main_do(self, duration=random.randint(3000, 4000), target_coin=10000, test=False):
        if test is True:
            self.main_do(duration, target_coin)
        else:
            t = time.time()
            while True:
                try:
                    self.main_do(duration, target_coin)
                    break
                except Exception as e:
                    self.logger.critical(f'出严重错误啦，以下是错误信息{e}', exc_info=True)
                    self.pp.screenshot(pathlib.Path.cwd() / 'log' / f'出错啦{random.random()}.jpg')
                    if time.time() - t > 3600:
                        self.logger.critical('程序存在错误，试了一个小时都不行，请修改程序')
                        self.app_end()
                        break
        self.del_watcher()

    def scroll_read_issue(self):
        self.pp.swipe(random.uniform(0.3, 0.7), random.uniform(0.7, 0.8), random.uniform(0.3, 0.7),
                      random.uniform(0, 0.2), steps=random.randint(20, 60))
        time.sleep(random.random() + 1)
        if random.random() < self.probability_scroll_up:
            self.pp.swipe(random.uniform(0.25, 0.7), random.uniform(0.15, 0.25),
                          random.uniform(0.25, 0.7), random.uniform(0.65, 0.8),
                          steps=random.randint(20, 60))
            time.sleep(random.random() + 1)
