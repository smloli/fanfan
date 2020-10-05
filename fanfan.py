# time:2020年8月9日13:48
# author:52loli
# 饭饭百合小说爬取
from lxml import etree
import requests as r
import os.path
import time
def get_html(url):
    html = s.get(url,headers = headers)
    html.encoding = 'gbk'
    return html.text

def get_xpath():
    space = '\u3000'
    mode = int(input('0.单本下载\t1.批量下载\nnum:'))
    # 判断下载模式
    if mode:
        # 批量下载
        num = input('0.下载全部\t1.下载前n本\nnum:')
        url = input('Url为空，默认为首页\nUrl:')
        if url=='':
            url = 'https://bbs.fanfann.com/thread.php?fid=117&type=49#tabA'
        html = etree.HTML(get_html(url))
        # 匹配全部帖子id
        url_id = html.xpath("//a[@name='readlink']/@href")[9:]
        # 判断是否选择下载前n本
        if num=='1':
            n = int(input('n:'))
            url_id = url_id[:n]
    else:
        # 单本下载
        b = 1
        url_id = []
        num = input(f'Url_{b}:')
        while(num!=''):
            url_id.append(num[24:])
            b += 1
            num = input(f'Url_{b}:')
    
    for c in url_id:
        start = time.time()
        html = etree.HTML(get_html(http + c))
        # 帖子id
        url_cid = html.xpath("//a[@style='color:green;']/@href")
        # 小说名
        novelName = html.xpath("//title/text()")
        novelName = novelName[0][:-18].replace('TXT下载 ','')
        # 访问在线阅读
        html = etree.HTML(get_html(http + url_cid[0]))
        # 下载路径
        path = '/storage/emulated/0/Download/' + novelName + '.txt'
        # 判断文件是否存在
        if os.path.exists(path):
            print(novelName + '，已下载！')
            continue
        # 文案
        wenan = html.xpath("//p[@class='intro']/text()")
        wenan = wenan[0].lstrip() + '\n'
        # 章节地址
        url = html.xpath("//ul[@class='cf']//li//a/@href")
        # 章节名
        title = html.xpath("//ul[@class='cf']//li//a/text()")
        # 标题计次
        i = 0
        # 下载进度
        j = 1
        # 去除文章简介
        url = url[1:]
        title = title[1:]
        lengh = len(url)
        print(f'正在下载:{novelName}')
        with open(path,'w',encoding = 'utf8') as f:
            f.write(wenan)
            for a in url:
                # 下载进度
                print(f'{j/lengh*100:.2f}%',end=' --> ',flush=True)
                # 正文
                html = etree.HTML(get_html(http + a))
                result = html.xpath('//div[@class="read-content j_readContent"]//text()')
                # 转换成字符串
                temp = ''.join(result)
                # 判断段落分隔符
                if space not in temp:
                    space = '    '
                else:
                    space = '\u3000'
                temp = temp.replace(space,'\n')
                f.write('\n' + title[i])
                f.write(temp)
                i+=1
                j+=1
        end = time.time()
        print(f'耗时:{end-start:.2f}s')
if __name__=='__main__':
    headers = {'UserAgent':'Mozilla/5.0 (Linux; Android 10; SM-G9880 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/84.0.4147.111 Mobile Safari/537.36'}
    http = 'https://bbs.fanfann.com/'
    s = r.session()
    get_xpath()
