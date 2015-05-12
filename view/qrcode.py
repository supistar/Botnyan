# -*- encoding:utf8 -*-

import csv
import cStringIO

from flask import Blueprint, request, abort, send_file

import settings
from model.googledrive import GoogleDrive
from model.qrcreator import QRCodeCreator


qrcode = Blueprint('qrcode', __name__, url_prefix='/qrcode')


@qrcode.route("/view", methods=['GET'])
def qr():
    params = request.args
    ids = params.get('id')
    if not ids:
        abort(404)
        return

    try:
        ids_num = int(ids)
    except:
        abort(404)
        return

    drive_kwargs = {
        'document_id': settings.QRCODE_DOCUMENT,
        'export_type': 'text/csv'
    }
    content = GoogleDrive().retrieve_content(**drive_kwargs)

    f = cStringIO.StringIO(content)
    reader = csv.reader(f, delimiter=',')
    next(reader)

    img = None
    for row in reader:
        print("Row : %r" % row)
        try:
            if int(row[0]) == ids_num:
                img = QRCodeCreator().create(row[2])
                break
        except:
            continue

    if not img:
        abort(404)
        return

    return send_file(img, mimetype='image/png')
