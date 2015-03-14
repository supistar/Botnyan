# -*- encoding:utf8 -*-

import os
import httplib2
import urllib
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build

from flask import Blueprint, request, Response, abort
from flask_negotiate import consumes
from flask.ext.cors import cross_origin

from model.parser import Parser
from model.utils import Utils

slack = Blueprint('slack', __name__, url_prefix='/api/slack')


@slack.route("/webhook", methods=['POST'])
@cross_origin()
@consumes('application/x-www-form-urlencoded')
def webhook():
    # For debug
    form = request.form
    print form

    # Check slack webhook token in request body
    request_token = Utils().parse_dic(form, 'token', 400)
    token = os.environ.get('SLACK_WEBHOOK_TOKEN')
    if not token or token != request_token:
        abort(401)

    # Parse request body
    username = Utils().parse_dic(form, 'user_name')
    trigger_word_uni = Utils().parse_dic(form, 'trigger_word')
    text_uni = Utils().parse_dic(form, 'text')

    if not username or 'bot' in username or not trigger_word_uni or not text_uni or urllib.unquote_plus(trigger_word_uni) != urllib.unquote_plus(text_uni):
        dic = {}
        return Response(Utils().dump_json(dic), mimetype='application/json')

    text = urllib.unquote_plus(text_uni)
    doc_id = Parser().get_document_id(text)
    if not doc_id:
        dic = {}
        return Response(Utils().dump_json(dic), mimetype='application/json')

    try:
        private_key = os.environ['GOOGLE_PRIVATE_KEY']
        if not private_key:
            abort(401)
        credentials = SignedJwtAssertionCredentials(os.environ['GOOGLE_CLIENT_EMAIL'],
                                                    private_key,
                                                    'https://www.googleapis.com/auth/drive',
                                                    sub=os.environ['GOOGLE_OWNER_EMAIL'])
        http = httplib2.Http()
        credentials.authorize(http)
        service = build('drive', 'v2', http=http)
        f = service.files().get(fileId=doc_id).execute()
        if 'exportLinks' in f and 'text/plain' in f['exportLinks']:
            download = f['exportLinks']['text/plain']
            resp, content = service._http.request(download)
        else:
            content = '読み込みに失敗したにゃー'
    except Exception as e:
        content = '読み込みに失敗したにゃーー : ' + str(e) + ' / ' + str(e.message)
    dic = {"text": content}
    return Response(Utils().dump_json(dic), mimetype='application/json')