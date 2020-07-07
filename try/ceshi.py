import socket, json, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests, time, random

# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
# headers = {'User-Agent': user_agent, 'Host': 'cl.5v6.xyz'}
# url2 = 'cl.ff0.xyz'
# url3 = 'http://172.67.131.109/index.php'
# headers = {'Host': url2}
# res = requests.get(url3, headers=headers, timeout=3)
# res.encoding = 'gbk'
# print(res.text)
#
# myaddr = socket.getaddrinfo(host=url2, port=80, family=socket.AF_INET)
# for j in myaddr:
#     print(j[4][0])
# print(myaddr)
#
# # print("https://cl.ff0.xyz/index.php"[-10:])
# thread = ThreadPoolExecutor(max_workers=60)
# dict1 = {}
# lock = threading.Lock()
#
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


with open('2.json', 'r', encoding='UTF-8') as f:
    p = json.load(f)
p1 = time.time()

with open('3.json', 'w', encoding='gbk') as f:
    json.dump(p, f)
# if (t1 := time.time()-p1) > 0.3:
#     print(t1)
print(time.time()-p1)
