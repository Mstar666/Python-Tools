# coding=gbk
# tcp_server.py
'''������'''

from socket import *
from time import ctime

HOST = '' #������ַ
PORT = 23345 #�˿ں�
BUFSIZ = 2048 #��������С����λ���ֽڣ������趨��2K�Ļ�����
ADDR = (HOST, PORT) #���ӵ�ַ

tcpSerSock = socket(AF_INET, SOCK_STREAM) #����һ��TCP�׽���
tcpSerSock.bind(ADDR) #�󶨵�ַ
tcpSerSock.listen(5) #���������Ϊ5

while True: #����ѭ��
    print('�������ӿͻ��ˡ�����')
    tcpCliSock, addr = tcpSerSock.accept() #�ȴ���������
    print('���ӳɹ����ͻ��˵�ַΪ��', addr)
    
    while True:
        data = tcpCliSock.recv(BUFSIZ) #��������,BUFSIZ�ǻ�������С
        if not data: break #���dataΪ�գ�������ѭ��
        print(data.decode())

        msg = '{} �������ѽ��� [�Զ��ظ�]'.format(ctime())
        tcpCliSock.send(msg.encode())
        
    tcpCliSock.close() #�ر�����

tcpSerSock.close() #�رշ�����