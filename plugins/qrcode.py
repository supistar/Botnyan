# -*- encoding:utf8 -*-

import csv
import cStringIO
import settings

from flask import url_for

from model.googledrive import GoogleDrive
from plugins.base.responsebase import IResponseBase


class QRCode(IResponseBase):

    def hear_regex(self, **kwargs):
        return "^(QRコード|QRCode)$"

    def response(self, **kwargs):
        drive_kwargs = {
            'document_id': settings.QRCODE_DOCUMENT,
            'export_type': 'text/csv'
        }
        content = GoogleDrive().retrieve_content(**drive_kwargs)

        f = cStringIO.StringIO(content)
        reader = csv.reader(f, delimiter=',')
        next(reader)

        attachments = []
        for row in reader:
            try:
                ids_num = int(row[0])
                description = row[1]
                attachment = {
                    "fallback": description,
                    "text": description,
                    "image_url": url_for('qrcode.qr', id=ids_num, _external=True),
                    "color": "#6698C8"
                }
                attachments.append(attachment)
            except:
                continue

        return {
            "text": "QRコードです n_n",
            "attachments": attachments
        }
