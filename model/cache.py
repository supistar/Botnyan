# -*- encoding:utf8 -*-

import os
import redis

from model.metaclass.singleton import Singleton


class Cache():

    __metaclass__ = Singleton
    rd = None

    def __init__(self):
        host = os.environ.get('REDIS_SERVER_HOST', 'localhost')
        port = os.environ.get('REDIS_SERVER_PORT', '6379')
        self.rd = redis.Redis(host=host, port=port, db=0)

    def set(self, key, value):
        self.rd.set(key, value)

    def get(self, key):
        return self.rd.get(key)

    def contains(self, key):
        return self.rd.exists(key)

    def clear(self, key):
        self.rd.delete(key)

    def keys(self):
        return self.rd.keys()