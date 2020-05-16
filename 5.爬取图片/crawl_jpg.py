#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.request
import urllib.parse
import os
#要先进行安装， pip install lxml
from lxml import etree
import time

def handle_request1(url,page):
    print("jaaj")
#构建请求对象
def handle_request(url, page):
    #由于第一页和后面的页码规律不一样，要判断
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

#解析内容并且下载图片
def parse_content(content):
    tree = etree.HTML(content)
    #最后一项为src就不行，懒加载？ what
    image_list = tree.xpath('//div[@id="container"]/div/div/a/img/@src2')
    print("image_list:",image_list)
    print('iamge_list len is :',len(image_list))
    #遍历列表一次下载
    for image_src in image_list:
        download_image(image_src)

def download_image(image_src):
    dirpath= 'xinggan'
    #创建文件夹
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    #文件mimg
    filename =os.path.basename(image_src)
    print("文件名:",filename)
    #文件路径
    filepath = os.path.join(dirpath,filename)
    print("文件路径:",filepath)
    #发送请求，保存图片
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
        print("下载成功")
def main():
    url = 'http://sc.chinaz.com/tupian/' \
          'xingganmeinvtupian{}.html'
    start_page = int(input('请输入起始图片页码：'))
    end_page = int(input('请输入结束图片页码：'))
    #start_page=1
    #end_page=10
    for page in range(start_page,end_page+1):
        request = handle_request(url,page)
        content=urllib.request.urlopen(request).read().decode()
        parse_content(content)
        print("第几页:",page)
        time.sleep(2)

if __name__ == '__main__':
    main()