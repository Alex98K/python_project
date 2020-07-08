import socket, json, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests, time, random, re
headers = {
'Cookie': '__cfduid = dedb7b74217ad13177da53c040882908d1594199084',
'Host': 'cl.5w9.xyz',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}
# user_agent = 'baidu'
# headers = {'User-Agent': user_agent, 'Host': 'cl.5v6.xyz'}
url2 = 'https://cl.5w9.xyz/thread0806.php?fid=16'
# url3 = 'http://172.67.131.109/index.php'
# headers = {'Host': url2}
res = requests.get(url2, headers=headers, timeout=31)
res.encoding = 'gbk'
print(res.text)


# thread = ThreadPoolExecutor(max_workers=60)
# dict1 = {}
# lock = threading.Lock()
'cookie: __cfduid=dc7860a61c3a696e9523a91ec028d913b1592741144; 227c9_lastvisit=0%091593765092%09%2Fthread0806.php%3Ffid%3D16%26search%3D%26page%3D49'

#
# def haha(int1):
#     # time.sleep(random.random())
#     dict1[str(int1)] = int1
#     # lock.acquire()
#     p1 = time.time()
#     with open('1.json', 'w', encoding='UTF-8') as f:
#         json.dump(dict1, f)
#     if (t1 := time.time()-p1) > 0.3:
#         print(t1)
#         # lock.release()
#
#
# for j in range(10000):
#     thread.submit(haha, j)
# thread.shutdown(wait=True)
#
# print(len(dict1))
#
# with open('1.json', 'r') as f:
#     p = json.load(f)
#     print(len(p))


# with open('2.json', 'r', encoding='UTF-8') as f:
#     p = json.load(f)
# p1 = time.time()
#
# with open('3.json', 'w', encoding='gbk') as f:
#     json.dump(p, f)
# # if (t1 := time.time()-p1) > 0.3:
# #     print(t1)
# print(time.time()-p1)
