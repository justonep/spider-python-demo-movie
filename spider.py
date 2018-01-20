from utils import get_page, build_xpath_tree, windows_name_format
from conn import RedisClient
from setting import *
import re
import redis


class DyttSpider(object):
    def __init__(self):
        self._conn = RedisClient()

    def menu(self):
        for i in range(1, 2):
            target_url = 'http://www.ygdy8.net/html/gndy/oumei/list_7_{}.html'.format(i)
            # 建立一个selector选择器，用于xpath过滤
            selector = build_xpath_tree(get_page(target_url, 'gb2312'))
            # 获取所有的子集页面的a标签
            items = selector.xpath('//div[@class="co_content8"]//tr//a[2]')
            # 提取a标签内的url和内容（电影名）
            for item in items:
                next_url = item.xpath('@href')[0]
                name = re.findall(u'《(.*)》', item.xpath('text()')[0])[0]
                print(name)
                self.get_info(next_url, movie_info={'name': windows_name_format(name)})

    def get_info(self, url, movie_info):
        selector = build_xpath_tree(get_page('http://www.ygdy8.net' + url, 'gb2312'))
        imgs = selector.xpath('//div[@id="Zoom"]//img/@src')
        urls = selector.xpath('//*[@id="Zoom"]//td/a/@href')
        movie_info['urls'] = urls
        movie_info['jpg'] = PHOTO_DIR + movie_info['name'] + '.jpg'
        try:
            self._conn.put(movie_info)
        except redis.exceptions.ConnectionError as RedisConnError:
            print('please check your redis.\n' + str(RedisConnError))
            exit()
        for img in imgs:
            img_bytes_file = get_page(img)
            try:
                with open(movie_info['jpg'], 'wb+') as img_file:
                    img_file.write(img_bytes_file)
            except TypeError as te:
                print('the movie name is null')
            except Exception as e:
                print(e)
