# -*- encoding:utf8 -*-

from abc import ABCMeta, abstractmethod


class IResponseBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def hear_regex(self, **kwargs):
        pass

    @abstractmethod
    def response(self, **kwargs):
        pass
