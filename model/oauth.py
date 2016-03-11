# -*- encoding:utf8 -*-

import os
from oauth2client.client import OAuth2WebServerFlow


class OAuth:

    def __init__(self):
        pass

    def get_flow(self):
        scope = 'https://www.googleapis.com/auth/drive'

        try:
            client_id = os.environ['GOOGLE_CLIENT_ID']
            client_secret = os.environ['GOOGLE_CLIENT_SECRET']
            base_url = os.environ['BOTNYAN_BASE_URL']
            separator = "/"
            if base_url.endswith("/"):
                separator = ""
            redirect_url = "{0}{1}api/drive/callback".format(base_url, separator)
            flow = OAuth2WebServerFlow(client_id=client_id,
                                       client_secret=client_secret,
                                       scope=scope,
                                       redirect_uri=redirect_url)
            return flow
        except:
            return None
