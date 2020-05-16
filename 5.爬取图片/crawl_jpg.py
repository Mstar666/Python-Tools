#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.request
import urllib.parse
import os
#Ҫ�Ƚ��а�װ�� pip install lxml
from lxml import etree
import time

def handle_request1(url,page):
    print("jaaj")
#�����������
def handle_request(url, page):
    #���ڵ�һҳ�ͺ����ҳ����ɲ�һ����Ҫ�ж�
    if page == 1:
        url = url.format('')
    else:
        url = url.format('_'+str(page))
    print(url)
    headers={
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0;'
                      ' Windows NT 6.1; WOW64; Trident/4.0; '
                      'SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729;'
                      ' .NET CLR 3.0.30729; Media Center PC 6.0)'
    }
    request = urllib.request.Request(url=url, headers=headers)
    return request

#�������ݲ�������ͼƬ
def parse_content(content):
    tree = etree.HTML(content)
    #���һ��Ϊsrc�Ͳ��У������أ� what
    image_list = tree.xpath('//div[@id="container"]/div/div/a/img/@src2')
    print("image_list:",image_list)
    print('iamge_list len is :',len(image_list))
    #�����б�һ������
    for image_src in image_list:
        download_image(image_src)

def download_image(image_src):
    dirpath= 'xinggan'
    #�����ļ���
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    #�ļ�mimg
    filename =os.path.basename(image_src)
    print("�ļ���:",filename)
    #�ļ�·��
    filepath = os.path.join(dirpath,filename)
    print("�ļ�·��:",filepath)
    #�������󣬱���ͼƬ
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0;'
                      ' Windows NT 6.1; WOW64; Trident/4.0; '
                      'SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729;'
                      ' .NET CLR 3.0.30729; Media Center PC 6.0)'
    }
    print('image_src:', image_src)
    request = urllib.request.Request(url=image_src, headers=headers)
    response = urllib.request.urlopen(request)
    with open(filepath, 'wb') as fp:
        fp.write( response.read())
        print("���سɹ�")
def main():
    url = 'http://sc.chinaz.com/tupian/' \
          'xingganmeinvtupian{}.html'
    start_page = int(input('��������ʼͼƬҳ�룺'))
    end_page = int(input('���������ͼƬҳ�룺'))
    #start_page=1
    #end_page=10
    for page in range(start_page,end_page+1):
        request = handle_request(url,page)
        content=urllib.request.urlopen(request).read().decode()
        parse_content(content)
        print("�ڼ�ҳ:",page)
        time.sleep(2)

if __name__ == '__main__':
    main()