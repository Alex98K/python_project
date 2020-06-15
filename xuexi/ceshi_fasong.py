import socket


def main():
    udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    lco = ('', 8800)
    udp_s.bind(lco)
    msg = input("输入内容：")
    udp_s.sendto(msg.encode("utf-8"), ("192.168.1.7", 8800))
    recv = udp_s.recvfrom(1024)
    recv_msg = recv[0].decode("utf-8")
    recv_addr = recv[1]
    print("来自{}的人发送了信息{}".format(str(recv_addr[0]), recv_msg))
    udp_s.close()


if __name__ == '__main__':
    main()
