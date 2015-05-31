# -*- encoding:utf8 -*-

from model.cache import Cache
from plugins.base.responsebase import IResponseBase


class CachePlugin(IResponseBase):

    def hear_regex(self, **kwargs):
        return '^%s\s+cache\s+--clear\s*$' % kwargs.get('botname')

    def response(self, **kwargs):
        Cache().clear_all()
        return {
            "text": "キャッシュをクリアしました n_n"
        }
