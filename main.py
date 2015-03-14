#!/usr/bin/env python
# -*- encoding:utf8 -*-

from flask import Flask
from flask.ext.cors import CORS
from api.slack import slack
from api.heartbeat import heartbeat

app = Flask(__name__)
app.register_blueprint(slack)
app.register_blueprint(heartbeat)
app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
cors = CORS(app)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge, chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == "__main__":
    app.run(debug=True)
