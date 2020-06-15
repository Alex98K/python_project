import socket
import select
import wsgi


class WebServer(object):
    def __init__(self):
        # 建立tcp套接字
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定端口和IP
        self.tcp_server.bind(("192.168.1.7", 9000))
        # 套接字设为监听
        self.tcp_server.listen(128)
        self.tcp_server.setblocking(False)
        # 创建epoll对象
        self.epl = select.epoll()
        self.epl.register(self.tcp_server.fileno(), select.EPOLLIN)

    def run(self):
        fd_event_dict = dict()
        while True:
            # epoll 等待接收到消息后，解除阻塞
            fd_event_list = self.epl.poll()
            for fd, event in fd_event_list:
                if fd == self.tcp_server.fileno():
                    # 等待接收
                    new_sock, addr = self.tcp_server.accept()
                    self.epl.register(new_sock.fileno(), select.EPOLLIN)
                    fd_event_dict[new_sock.fileno()] = new_sock
                elif event == select.EPOLLIN:
                    rev_data = fd_event_dict[fd].recv(1024).decode("utf-8")
                    if rev_data:
                        # 开始服务
                        response = wsgi.wsgi_work(rev_data, addr)
                        fd_event_dict[fd].sendall(response.encode("utf-8"))
                    else:
                        fd_event_dict[fd].close()
                        self.epl.unregister(fd)
                        del fd_event_dict[fd]

    def __del__(self):
        self.tcp_server.close()


def main():
    run_s = WebServer()
    run_s.run()


if __name__ == '__main__':
    main()
