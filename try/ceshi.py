import re

pattern = re.compile(r'\[(\d{1,3})P.*?\]|(\d{1,3})P.{1,3}\]|\[(\d{1,3})P|\[(\d{1,3})\]')
st = '[控丝原创]第七期，小母狗穿着狼友挑选的情趣黑丝配婚鞋展现风骚的一面[16]'

print([j for j in re.search(pattern, st).groups() if j][0])
