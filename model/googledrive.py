# -*- encoding:utf8 -*-

import os
import httplib2
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build


class GoogleDrive(object):

    @classmethod
    def retrieve_content(cls, **kwargs):
        document_id = kwargs.get('document_id')
        export_type = kwargs.get('export_type')

        if not document_id:
            print("There is no documentID")
            return None
        if not export_type:
            print("There is no exportType")
            return None

        try:
            private_key = os.environ['GOOGLE_PRIVATE_KEY']
            if not private_key:
                return None

            credential_args = (
                os.environ['GOOGLE_CLIENT_EMAIL'],
                private_key,
                'https://www.googleapis.com/auth/drive'
            )
            credential_kwargs = {
                'sub': os.environ.get('GOOGLE_OWNER_EMAIL')
            }
            credentials = SignedJwtAssertionCredentials(*credential_args, **credential_kwargs)
            http = httplib2.Http()
            credentials.authorize(http)
            service = build('drive', 'v2', http=http)
            f = service.files().get(fileId=document_id).execute()
            if 'exportLinks' in f and export_type in f['exportLinks']:
                download = f['exportLinks'][export_type]
                resp, content = service._http.request(download)
            else:
                content = '読み込みに失敗したにゃー'
        except Exception as e:
            content = '読み込みに失敗したにゃーー : ' + str(e) + ' / ' + str(e.message)
        return content
