# -*- encoding:utf8 -*-

from model.parser import Parser
from plugins.base.responsebase import IResponseBase


class Lists(IResponseBase):

    def hear_regex(self, **kwargs):
        return ('^%s\s+list(|s)\s*$' % kwargs.get('botname'))

    def response(self, **kwargs):
        return {"text": "登録ドキュメントID・キーワード一覧です n_n\n```- {0}```".format("\n- ".join(Parser().get_documentid_keyword_list()))}
