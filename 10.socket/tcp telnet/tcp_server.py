# coding=gbk
# tcp_server.py
'''服务器'''

from socket import *
from time import ctime

HOST = '' #主机地址
PORT = 23345 #端口号
BUFSIZ = 2048 #缓存区大小，单位是字节，这里设定了2K的缓冲区
ADDR = (HOST, PORT) #链接地址

tcpSerSock = socket(AF_INET, SOCK_STREAM) #创建一个TCP套接字
tcpSerSock.bind(ADDR) #绑定地址
tcpSerSock.listen(5) #最大连接数为5

while True: #无限循环
    print('尝试连接客户端。。。')
    tcpCliSock, addr = tcpSerSock.accept() #等待接受连接
    print('链接成功，客户端地址为：', addr)
    
    while True:
        data = tcpCliSock.recv(BUFSIZ) #接收数据,BUFSIZ是缓存区大小
        if not data: break #如果data为空，则跳出循环
        print(data.decode())

        msg = '{} 服务器已接收 [自动回复]'.format(ctime())
        tcpCliSock.send(msg.encode())
        
    tcpCliSock.close() #关闭连接

tcpSerSock.close() #关闭服务器