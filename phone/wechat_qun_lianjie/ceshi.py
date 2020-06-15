import requests, re

url = 'https://mp.weixin.qq.com/s/wPl94ZO1xllWV06qValMJw'
# url1 = 'http://dw.chinanews.com/chinanews/content.jsp?id=9084978&classify=zw&pageSize=6&language=chs&from=groupmessage=jpg'
p = requests.get(url).text
pattern = r'"(http.*?[\.|=](jpeg|png|jpg|gif))"'


print(re.findall(pattern, p))

