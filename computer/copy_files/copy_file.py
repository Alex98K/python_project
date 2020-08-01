# -*- coding: utf-8 -*-
import os
import shutil


class CopyFile(object):
    def __init__(self, path_ore, path_des, exchange=False):
        if exchange:
            # 是否要源文件夹和目标文件夹交换再拷贝
            path_ore, path_des = path_des, path_ore
        self.path_ore = path_ore
        self.path_des = path_des
        self.all_size = 0
        self.sum_size = 0

    def get_dir_size(self):  # 计算文件夹大小
        sum_1 = 0
        for root1, dirs, files1 in os.walk(self.path_ore):
            for file1 in files1:
                sum_1 += os.stat(os.path.join(root1, file1)).st_size
        return sum_1

    def main(self):
        self.all_size = self.get_dir_size()
        for root, dir2, files in os.walk(self.path_ore):
            for dir_o in dir2:
                ore_dir = os.path.join(root, dir_o)
                des_dir = ore_dir.replace(self.path_ore, self.path_des)
                if not os.path.exists(des_dir):
                    os.makedirs(des_dir)
            for file in files:
                ore_file = os.path.join(root, file)
                des_file = ore_file.replace(self.path_ore, self.path_des)
                size = os.stat(ore_file).st_size
                self.sum_size += size
                process = "\r[共有%.2fGB, 剩余%.2fGB, 完成进度%.5s%%]: |%-50s|" % \
                          (self.all_size / (1024 * 1024 * 1024),
                           (self.all_size - self.sum_size) / (1024 * 1024 * 1024),
                           self.sum_size / self.all_size * 100,
                           '|' * int(self.sum_size / self.all_size * 50))
                if not os.path.exists(des_file):
                    print(process + f'  准备拷贝文件：{ore_file}', end='', flush=True)
                    shutil.copy2(ore_file, des_file)
                elif os.stat(ore_file).st_mtime > os.stat(des_file).st_mtime:
                    print(process + f'  ！覆盖！准备拷贝文件：{ore_file}', end='', flush=True)
                    shutil.copy2(ore_file, des_file)
                else:
                    print(process + f'  跳过这个文件：{ore_file}', end='', flush=True)
        print('\n', end='\n', flush=True)
        print('拷贝完成！', end='\n', flush=True)


if __name__ == '__main__':
    # do = CopyFile(path_ore=r"F:/D/", path_des=r"D:/工作/D/", exchange=False)
    do = CopyFile(path_ore=r"F:/D/", path_des=r"D:/工作/D/", exchange=True)
    do.main()
