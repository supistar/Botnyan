# -*- encoding:utf8 -*-

from model.parser import Parser
from model.googledrive import GoogleDrive
from plugins.base.responsebase import IResponseBase


class Drive(IResponseBase):

    def hear_regex(self, **kwargs):
        lists = Parser().get_keyword_list(expand=True)
        print("Lists : %r" % lists)
        return "^({0})$".format("|".join(lists))

    def response(self, **kwargs):
        drive_kwargs = {
            'document_id': Parser().get_document_id(kwargs.get('text')),
            'export_type': 'text/plain'
        }
        return GoogleDrive().retrieve_content(**drive_kwargs)
