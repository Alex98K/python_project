import re


url_one = 'https://www.sinaimg.cn/dy/slidenews/32_img/2016_33/35533_5251718_971332.gif'
style = re.search(r'\.\w*$', url_one).group()
print(style)