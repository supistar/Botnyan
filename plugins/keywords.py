# -*- encoding:utf8 -*-

from model.parser import Parser
from plugins.base.responsebase import IResponseBase


class Keywords(IResponseBase):

    def hear_regex(self, **kwargs):
        return ('^%s\s+keyword(|s)\s*$' % kwargs.get('botname'))

    def response(self, **kwargs):
        return {"text": "登録キーワード一覧です n_n\n```- {0}```".format("\n- ".join(Parser().get_keyword_list()))}
