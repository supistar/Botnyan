# -*- encoding:utf8 -*-

import httplib2
from flask import Blueprint, redirect, request, Response, abort

from model.oauth import OAuth
from model.utils import Utils


drive = Blueprint('drive', __name__, url_prefix='/drive')


@drive.route("/auth", methods=['GET'])
def hookauth():
    flow = OAuth().get_flow()
    if not flow:
        abort(500)
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)


@drive.route("/callback", methods=['GET'])
def callback():
    try:
        code = request.args['code']
    except:
        abort(400)
    flow = OAuth().get_flow()
    credentials = flow.step2_exchange(code)
    http = httplib2.Http()
    credentials.authorize(http)
    dic = {"response": "success"}
    return Response(Utils().dump_json(dic), mimetype='application/json')
