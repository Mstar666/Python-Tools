#coding=gbk
#udp-client.py
'''�ͻ���'''

from socket import *

host = 'localhost'  #���ط�������ַ
port = 12345  #�ͻ��˶˿�(ȷ���ͷ������Ķ˿�һ��
bufsiz = 2048 #�����С
addc = (host, port) #��ַ+�˿�

udpclisock = socket(AF_INET, SOCK_DGRAM)  #����UDP���׽������͡�

while True:
    msg = input('�ͻ���˵��')    #��������
    udpclisock.sendto(msg.encode('utf-8'), addc)
    data, adds = udpclisock.recvfrom(bufsiz)
    
    if not data: break
    print('�������ش�', data.decode('utf-8'))
    
udpclisock.close()

print('Exit Client!')