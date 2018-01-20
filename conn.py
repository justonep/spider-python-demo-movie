from setting import *
import redis


class RedisClient(object):

    def __init__(self,host=HOST,port=PORT,password=PASSWORD):
        if PASSWORD:
            self._db = redis.Redis(host=host,port=port,password=password)
        else:
            self._db = redis.Redis(host=host,port=port)
        print('redis connect success')

    def put(self,proxy):
        self._db.rpush("movie_info",proxy)




