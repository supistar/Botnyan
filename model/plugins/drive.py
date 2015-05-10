# -*- encoding:utf8 -*-

import os
import httplib2
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build

from model.parser import Parser
from model.plugins.base.responsebase import IResponseBase


class Drive(IResponseBase):

    def hear_regex(self, **kwargs):
        lists = Parser().get_keyword_list(expand=True)
        print("Lists : %r" % lists)
        return "^({0})$".format("|".join(lists))

    def response(self, **kwargs):
        document_id = Parser().get_document_id(kwargs.get('text'))
        if not document_id:
            print("There is no documentID")
            return None

        print("documentID :) / %r" % document_id)
        try:
            private_key = os.environ['GOOGLE_PRIVATE_KEY']
            if not private_key:
                return {}
            credentials = SignedJwtAssertionCredentials(os.environ['GOOGLE_CLIENT_EMAIL'],
                                                        private_key,
                                                        'https://www.googleapis.com/auth/drive',
                                                        sub=os.environ['GOOGLE_OWNER_EMAIL'])
            http = httplib2.Http()
            credentials.authorize(http)
            service = build('drive', 'v2', http=http)
            f = service.files().get(fileId=document_id).execute()
            if 'exportLinks' in f and 'text/plain' in f['exportLinks']:
                download = f['exportLinks']['text/plain']
                resp, content = service._http.request(download)
            else:
                content = '読み込みに失敗したにゃー'
        except Exception as e:
            content = '読み込みに失敗したにゃーー : ' + str(e) + ' / ' + str(e.message)
        return content
