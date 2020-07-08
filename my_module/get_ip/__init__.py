import re
import requests
import socket


def get_ip():
    response = requests.get('http://www.baidu.com/s?wd=ip')
    html = response.text
    res = re.compile('fk="(.*?)"').findall(html)
    return res[0]


def url_to_ip(url):
    my_addr_r = []
    if 'https://' in url:
        url = re.search('https://(.*?)/', url).group(1)
    elif 'http://' in url:
        url = re.search('http://(.*?)/', url).group(1)
    try:
        my_addr = socket.getaddrinfo(host=url, port=None)
    except socket.gaierror:
        print('请输入正确的URL地址https://www.baidu.com/......或者http://www.baidu.com/......或者www.baidu.com')
        raise
    for j in my_addr:
        my_addr_r.append(j[4][0])
    return my_addr_r


if __name__ == '__main__':
    print(get_ip())
    print(url_to_ip('https://cl.5w9.xyz/index.php'))
