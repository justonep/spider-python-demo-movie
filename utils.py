import requests
from fake_useragent import UserAgent
from lxml import etree
'''chardet.detect(str)可以去自动判别编码'''
import chardet
import http

def get_page(url,encoding=0,**options):
    """
    返回decode后的网页，或者bytes文件
    :param url:
    :param encoding:如果不提供encoding，将返回bytes文件
    :param options:接收一些需要添加到cookies的字典文件
    :return: 用于获取网页的html代码
    """

    # 获取一个随机的useragent
    useragents = UserAgent()
    base_headers = {
        'User-Agent':  useragents.random,
    }
    # 以应对不同网站可能需要特定的参数 ，如 cookies，oauth之类的参数，保证代码的重复利用
    base_headers = dict(base_headers, **options)
    try:
        result=requests.get(url,headers=base_headers)
        print('get {} success,the result code is {}'.format(url,result.status_code))
        if result.status_code == 200:
            if encoding:
                return result.content.decode(encoding)
            else:
                return result.content

    except ConnectionError:
        print('connect error')

    # 当解码时发生异常，忽略异常部分的部分文字
    except UnicodeDecodeError as DecodeDo:
        warning = 'download models decode happen some errors,'+str(DecodeDo)+'\n'+url
        print(warning)
        return result.content.decode(encoding,'ignore')

    # 由于user-agent导致的被服务器拒绝
    except http.client.RemoteDisconnected as ConnDo:
        print('{} connection error ,restart.'.format(url)+str(ConnDo))
        get_page(url, encoding, **options)

def build_xpath_tree(html):
    """

    :param html:
    :return: 返回一个选择器，注意是一个列表
    """
    selector = etree.HTML(html)
    return selector


def windows_name_format(name):
    """
    由于windows禁止部分字符作为文件名
    :param name:
    :return: 返回一个不包含   < > / \ | : " * ?的字符串
    """

    invalid_chars = ['<', '>', '/', '\\', ':', '"', '*']
    for char in invalid_chars:
        name = name.replace(char, '')
    return name