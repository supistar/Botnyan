# -*- encoding:utf8 -*-

import cStringIO
import qrcode


class QRCodeCreator():

    def __init__(self):
        pass

    def create(self, message):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(message)
        qr.make(fit=True)
        img = qr.make_image()

        img_buf = cStringIO.StringIO()
        img.save(img_buf)
        img_buf.seek(0)
        return img_buf
