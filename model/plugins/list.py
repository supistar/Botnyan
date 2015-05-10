# -*- encoding:utf8 -*-

from model.plugins.base.responsebase import IResponseBase
from model.parser import Parser


class Lists(IResponseBase):

    def hear_regex(self, **kwargs):
        return ('^%s\s+list(|s)\s*$' % kwargs.get('botname'))

    def response(self, **kwargs):
        return {"text": "登録ドキュメントID・キーワード一覧です n_n\n```- {0}```".format("\n- ".join(Parser().get_documentid_keyword_list()))}
