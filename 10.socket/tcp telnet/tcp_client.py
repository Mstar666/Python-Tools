# coding=gbk
# tcp_client.py
'''�ͻ���'''

from socket import *
from time import ctime

HOST = 'localhost' #������ַ
PORT = 23345 #�˿ں�
BUFSIZ = 2048 #��������С����λ���ֽڣ������趨��2K�Ļ�����
ADDR = (HOST, PORT) #���ӵ�ַ

tcpCliSock = socket(AF_INET, SOCK_STREAM) #����һ��TCP�׽���
#tcpCliSock.bind(ADDR) #�󶨵�ַ
tcpCliSock.connect(ADDR) #�󶨵�ַ

while True:
    msg = input('������:') #��������
    if not msg: break #��� msg Ϊ�գ�������ѭ��
    tcpCliSock.send(msg.encode())
    
    data = tcpCliSock.recv(BUFSIZ) #��������,BUFSIZ�ǻ�������С
    if not data: break #���dataΪ�գ�������ѭ��
    print(data.decode())