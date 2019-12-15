import socket
import re
from multiprocessing import Process 
import time
import dynamic.mini_frame


class WSGIServer(object):
    def __init__(self):
        '''用来完成整体的控制'''
        # 创建套接字
        self.web_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.web_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定
        self.web_server.bind(("127.0.0.1", 8080))
        # 变为监听套接字
        self.web_server.listen(5)
                

    def service_client(self, client):
        #接收流览器发过来的请求
        #GET / HTTP/1.1
        #.......
        request = client.recv(1024).decode('utf-8')
            
        request_lines = request.splitlines()
        #print(request.decode('utf-8'))

        print(request_lines)
        print(">>>"*20)

        file_name = ""
        #如果发送数据空，则直接结束
        #正则匹配TCP头的参数
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
        #如果ret不为空，返回后缀
        if ret:
            file_name = ret.group(1)
            if file_name == "/":
                file_name = "/index.html"
        
        #返回浏览器请求的数据

        #打开客户请求的页面
        #非.py结尾的请求资源则认为是静态资源(html\css\js等)
        if not file_name.endswith(".py"):
            try:
                f = open("./static"+file_name, "rb")
            except:
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                response += "------------not found------------"
                client.send(response.encode('utf-8'))
            else:
                html_content = f.read()
                f.close()
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
          
                client.send(response.encode('utf-8'))
                client.send(html_content)
        else:
            #如果是以.py结尾的请求资源，则认为是动态资源

            env = dict()
            
            env['PATH_INFO'] = file_name

            body = dynamic.mini_frame.application(env, self.set_response_header)

            header = "HTTP.1.1 %s\r\n" % self.status

            self.header += [('server', 'mini-server v1.0')]

            for temp in self.header:
                header += "%s:%s\r\n" % (temp[0], temp[1])
            
            header += "\r\n"

            response = header + body

            client.send(response.encode('utf-8'))
        
        #关闭套接字
        client.close()


    def set_response_header(self, status, header):
        self.status = status
        self.header = header


    def run_forever(self):
        while True:
            # 等待新客户端的链接
            client, addr = self.web_server.accept() 
            # 为这个客户提供服务
            p = Process(target=self.service_client, args=(client,))
            p.start()
            client.close()
            #service_client(client)
        #关闭监听套接字
        self.web_server.close()

def main():
    wsgi_server = WSGIServer()
    wsgi_server.run_forever()

if __name__ == "__main__":
    main()
