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
        self.probability_scroll_up = 0.05  # 看视频或文章向上滑动（回看）的概率
        self.probability_thumb_up = 0.1  # 点赞概率
        self.probability_commit = 0.03  # 评论概率
        self.probability_focus = 0.02  # 关注概率
        self.path = pathlib.Path().cwd()
        self.logger = self.log_config(phone_serial)
        with open(self.path / 'conf' / 'app_info.json', 'r', encoding='UTF-8') as f:
            self.app_info = json.load(f)
        with open(self.path / 'conf' / 'commit.json', 'r', encoding='UTF-8') as f:
            self.commit = json.load(f)
        if not pathlib.Path(pathlib.Path.cwd() / 'log' / 'screenshot').exists():
            pathlib.Path(pathlib.Path.cwd() / 'log' / 'screenshot').mkdir(parents=True)
        self.package_name = ''
        self.app_name = ''
        # self.pp.watcher('init1').when('我知道了').click()
        # self.pp.watcher('init2').when('知道了').click()
        # self.pp.watcher('init3').when(xpath='//*[contains(@resource-id, "close")]').click()

    def app_start(self, app_name):
        self.app_name = app_name
        app_list_running, app_install_list = self.pp.app_list_running(), self.pp.app_list()
        for k, v in self.app_info.items():
            if v[1] == app_name:
                self.package_name = k
                if k not in app_install_list:
                    self.logger.info(f'********没有安装 {app_name} 软件，结束********')
                    raise UserExceptionAppPass
                if k in app_list_running:
                    self.pp.app_stop(k)
                self.pp.app_start(k)
                self.logger.info(f'********开始 {app_name} 的任务********')
                return
        self.logger.error('app名字输入错误，无法启动app')
        raise UserExceptionAppPass

    def app_end(self):
        self.pp.app_stop(self.package_name)
        self.logger.info(f'********结束 {self.app_name} APP 任务********')

    def app_switch_current(self):
        if self.pp.app_current() != self.package_name:
            self.pp.app_start(self.package_name)

    def log_config(self, phone_serial):
        # 设置log
        logger = logging.getLogger(f"{phone_serial}_logger")
        if not logger.handlers:
            logger.setLevel(level=logging.DEBUG)
            # StreamHandler 输出到控制台的logger
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(level=logging.INFO)
            logger.addHandler(stream_handler)
            # FileHandler 输出到文件的logger
            if not pathlib.Path(self.path / 'log').exists():
                pathlib.Path.mkdir(self.path / 'log')
            file_handler = logging.FileHandler(self.path / 'log' / f'{phone_serial}_log.txt',
                                               mode='a', encoding='UTF-8')
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

    def main_do(self, duration, target_coin, cash_out):
        pass

    def cash_out(self, cash_out):
        if not cash_out:
            return

    def del_watcher(self):
        try:
            self.pp.watcher.stop()
            self.pp.watcher.remove()
        except AttributeError:
            self.logger.error('程序结束调用del注销watcher出错')

    def recycle_main_do(self, duration=3600, target_coin=10000, cash_out=False, test=False):
        if test is True:
            self.main_do(duration, target_coin, cash_out)
        else:
            t = time.time()
            while True:
                try:
                    self.main_do(duration, target_coin, cash_out)
                    break
                except UserExceptionAppPass:
                    break
                except Exception as e:
                    self.logger.critical(f'出严重错误啦，以下是错误信息{e}', exc_info=True)
                    struct_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
                    self.pp.screenshot(pathlib.Path.cwd() / 'log' / 'screenshot' /
                                       f'{self.phone_serial}_{struct_time}.jpg')
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

    def scroll_read_novel(self):
        self.pp.swipe(random.uniform(0.6, 0.85), random.uniform(0.75, 0.85),
                      random.uniform(0.15, 0.35), random.uniform(0.75, 0.85),
                      steps=random.randint(20, 60))
        time.sleep(random.random() + 1)
        if random.random() < self.probability_scroll_up * 0.1:
            self.pp.swipe(random.uniform(0.15, 0.35), random.uniform(0.75, 0.85),
                          random.uniform(0.6, 0.85), random.uniform(0.75, 0.85),
                          steps=random.randint(20, 60))
            time.sleep(random.random() + 1)


class UserExceptionAppPass(Exception):
    def __init__(self):
        super(UserExceptionAppPass, self).__init__()

    def __str__(self):
        return '程序存在错误,跳过运行这个APP'
