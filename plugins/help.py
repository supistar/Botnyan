# -*- encoding:utf8 -*-

from plugins.base.responsebase import IResponseBase


class Help(IResponseBase):

    def hear_regex(self, **kwargs):
        return ('^%s\s+help\s*$' % kwargs.get('botname'))

    def response(self, **kwargs):
        return {
            "text": "ヘルプです n_n\n"
            + "```"
            + "- botnyan keyword(s) : 登録されているキーワードを表示します\n"
            + "- botnyan list : 登録されているキーワードとドキュメントIDを表示します\n"
            + "- {登録されているキーワード} : キーワードに対応したドキュメントIDをもとに、Google Drive の内容を取得し表示します"
            + "```"
        }
