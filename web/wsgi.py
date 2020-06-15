import web_frame
import re


class WSGIServer(object):
    def set_env(self, data, addr):
        location = re.search(r' .*? ', data).group()
        env = {
            "issue": data,
            "ip": addr[0],
            "port": addr[1],
            "location": location
        }
        return env

    def set_response_header(self, status, reh):
        header = 'HTTP/1.1 ' + status
        for k, v in reh.items():
            header += "\r\n" + k + v
        # 'HTTP/1.1 200 OK \r\nContent-Type:text/html\r\nContent-length:50'
        self.header = str(header)

    def wsgi_job(self, data, addr):
        # 为客户端服务 , 准备数据
        env = self.set_env(data, addr)
        body = web_frame.application(env, self.set_response_header)
        response = self.header + "\r\n\r\n" + body
        # 返回http格式数据
        return response


def wsgi_work(data, addr):
    wsgi_s = WSGIServer()
    return wsgi_s.wsgi_job(data, addr)

