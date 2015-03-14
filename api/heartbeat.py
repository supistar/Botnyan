# -*- encoding:utf8 -*-

from flask import Blueprint, Response
from flask.ext.cors import cross_origin

from model.utils import Utils

heartbeat = Blueprint('heartbeat', __name__, url_prefix='/api')


@heartbeat.route("/heartbeat", methods=['GET'])
@cross_origin()
def beat():
    dic = {'status': 'OK'}
    return Response(Utils().dump_json(dic), mimetype='application/json')
