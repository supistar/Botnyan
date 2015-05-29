# -*- encoding:utf8 -*-

import os
import redis
from redis.exceptions import ConnectionError

import settings
from model.exceptions import CacheError
from model.metaclass.singleton import Singleton


class Cache():

    __metaclass__ = Singleton
    rd = None

    def __init__(self):
        host = os.environ.get('REDIS_SERVER_HOST', 'localhost')
        port = os.environ.get('REDIS_SERVER_PORT', '6379')
        self.rd = redis.Redis(host=host, port=port, db=0)

    def set(self, key, value):
        if not settings.USE_CACHE:
            return
        try:
            self.rd.set(key, value)
        except ConnectionError as e:
            raise CacheError(e)

    def get(self, key):
        if not settings.USE_CACHE:
            return None
        try:
            return self.rd.get(key)
        except ConnectionError as e:
            raise CacheError(e)

    def contains(self, key):
        if not settings.USE_CACHE:
            return False
        try:
            return self.rd.exists(key)
        except ConnectionError as e:
            raise CacheError(e)

    def clear(self, key):
        if not settings.USE_CACHE:
            return
        try:
            self.rd.delete(key)
        except ConnectionError as e:
            raise CacheError(e)

    def keys(self):
        if not settings.USE_CACHE:
            return
        try:
            return self.rd.keys()
        except ConnectionError as e:
            raise CacheError(e)
