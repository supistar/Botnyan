# -*- encoding:utf8 -*-

import os
import urllib
import re

from flask import Blueprint, request, Response, abort
from flask_negotiate import consumes
from flask.ext.cors import cross_origin

import settings
from model.utils import Utils
from model.loader import PluginLoader

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

    # Check trigger user is not bot
    if not username or 'bot' in username:
        dic = {}
        return Response(Utils().dump_json(dic), mimetype='application/json')

    botname = settings.BOTNAME
    if not botname:
        abort(500)

    re_flags = settings.RE_FLAGS
    plugins = PluginLoader().get_plugins()
    content = None
    kwargs = {
        'text': text_uni,
        'trigger_word': trigger_word_uni,
        'botname': botname
    }
    for plugin in plugins:
        regex_uni = Utils().convert_unicode(plugin().hear_regex(**kwargs))
        print("Using plugin : %r" % plugin)
        print("Using regex : %r" % regex_uni)
        print("Target text : %r" % urllib.unquote_plus(text_uni))
        if re.compile(regex_uni, re_flags).match(urllib.unquote_plus(text_uni)):
            print("Regex found :)")
            content = plugin().response(**kwargs)
            break

    if not content:
        dic = {}
    else:
        dic = {"text": content}
    return Response(Utils().dump_json(dic), mimetype='application/json')
