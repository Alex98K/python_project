import re, requests


url_one = 'https:\\f<>|?'
style = re.sub(r'[/\\:*?\"<>|]', '', url_one)
print(style)
