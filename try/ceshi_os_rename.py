import os
import re

path = 'D:\python书'
pp = os.listdir(path)
for i in pp:
    res = re.match(r'\[.*\]\.', i)
    if res:
        rest = re.sub(r'\[.*\]\.', '', i)
        # print(rest)
        try:
            os.renames(os.path.join(path, i), os.path.join(path, rest))
        except FileExistsError as e:
            os.remove(os.path.join(path, i))
            print(i)
