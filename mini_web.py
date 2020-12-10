import socket
import threading
import sys
import framework


class HTTPServer:
    def __init__(self, port):
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        tcp_server.bind(('', port))
        tcp_server.listen(128)
        self.tcp_server = tcp_server

    @staticmethod
    def handle_client(new_socket):
        # 接收客户端的请求信息
        recv_data = new_socket.recv(4096).decode('utf-8')
        # 如果recv_data没有信息，后面代码中切片取值会报错，所以要检测一下是否为空值
        if not recv_data:
            new_socket.close()
            return
        file_path = recv_data.split('\r\n', maxsplit=2)[0].split(' ')[1]
        print(file_path)
        # 如果没跟详细地址，则返回首页
        # if file_path == '/':
        #     file_path = '/index.html'
        file_path = '/index.html' if file_path == '/' else file_path
        # 判断是否是动态资源请求
        if file_path.endswith('.html'):
            env = {
                'request_path': file_path
            }
            status, headers, response_body = framework.handle_request(env)
            print(status, headers)
            # 响应行
            response_line = 'HTTP/1.1 200 %s\r\n' % status
            # 响应头
            response_header = ''
            for header in headers:
                response_header += '%s: %s\r\n' % header
            # 响应报文
            response_data = (response_line + response_header + '\r\n' + response_body).encode('utf-8')
            new_socket.send(response_data)
            new_socket.close()
            return

        try:
            # 打开文件
            with open('static' + file_path, 'rb') as file:
                file_data = file.read()
            # 响应行
            response_line = 'HTTP/1.1 200 OK\r\n'
            # 响应头
            response_header = 'Server: PWS/1.1\r\n'
            # 响应体
            response_body = file_data
            # 把数据封装成HTTP 响应报文格式的数据
            # 因为打开方式以rb模式打开，file_data为二进制格式，所以需要把响应行，响应头，和空行直接转换成二进制然后返回套接字
            # 发送给浏览器的套接字
        except FileNotFoundError:
            # 响应行
            response_line = 'HTTP/1.1 404 Not Found\r\n'
            # 响应头
            response_header = 'Server: PWS/1.1\r\n'
            with open('static/error.html', 'rb') as file:
                file_data = file.read()
            response_body = file_data

        finally:
            response = (response_line + response_header + '\r\n').encode('utf-8') + response_body

            new_socket.send(response)
            new_socket.close()

    def run(self):
        while True:
            try:
                new_socket, ip_port = self.tcp_server.accept()
                threading_task = threading.Thread(target=self.handle_client, args=(new_socket,), daemon=True)
                threading_task.start()
            except KeyboardInterrupt:
                sys.exit()


def main():
    # # 判断命令行参数是否为2
    # if len(sys.argv) != 2:
    #     print('请以类似格式运行 python mini_web.py 9000')
    #     return
    # # 判断字符串是否是由数字组成
    # if not sys.argv[1].isdigit():
    #     print('请以类似格式运行 python mini_web.py 9000')
    #     return
    # # 获取终端命令行参数
    # port = int(sys.argv[1])
    # 创建web server对象
    server = HTTPServer(9000)
    # 启动web server对象
    server.run()


if __name__ == '__main__':
    main()
