import re


url_one = 'https://www.sinaimg.cn/dy/slidenews/32_img/2016_33/35533_5251718_971332.gi\\f<>|?'
style = re.sub(r'[\/\\\:\*\?\"\<\>\|]', '', url_one)
print(style)