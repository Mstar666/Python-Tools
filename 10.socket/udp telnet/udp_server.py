# coding=gbk
#udp-server.py
'''������'''

from socket import *

host = ''  #��������ַ
port = 12345  #�������˿�
bufsiz = 2048 #�����С
adds = (host, port) #��ַ+�˿�

udpsersock = socket(AF_INET, SOCK_DGRAM)  #����UDP���׽������͡�
udpsersock.bind(adds)  #�󶨵���ַ�Ͷ˿�

while True:
    msg = input('������˵��')    #��������
    data, addc = udpsersock.recvfrom(bufsiz)
    udpsersock.sendto(msg.encode('utf-8'), addc)
    
    if not data: break
    print('�ͻ��˻ش�', data.decode('utf-8'))
    
udpsersock.close()