import json

import flask
from flask import make_response
from werkzeug.exceptions import HTTPException

app = flask.Flask(__name__)

data = dict()


@app.route('/hello', methods=['GET'])
def hello_handler():
    res = make_response("HSE OneLove!", 200)
    res.content_type = 'text/plain'
    return res


@app.errorhandler(HTTPException)
def handle_exception(e):
    return make_response("", 405)


@app.route('/set', methods=['POST'])
def set_key_value():
    if 'Content-Type' not in flask.request.headers or flask.request.headers['Content-Type'] != 'application/json':
        return make_response("", 415)
    if not flask.request or 'key' not in flask.request.json or 'value' not in flask.request.json:
        return make_response("", 400)
    data[flask.request.json['key']] = flask.request.json['value']
    return make_response("", 200)


@app.route('/get/<key>', methods=['GET'])
def get_key_handler(key):
    if key not in data:
        return make_response("", 404)
    res = make_response(json.dumps({'key': key, 'value': data[key]}), 200)
    res.content_type = 'application/json'
    return res


@app.route('/devide', methods=['POST'])
def devide_handler():
    if 'Content-Type' not in flask.request.headers or flask.request.headers['Content-Type'] != 'application/json':
        return make_response("", 415)
    if not flask.request or 'dividend' not in flask.request.json or 'divider' not in flask.request.json or \
            flask.request.json['divider'] == 0:
        return make_response("", 400)
    res = make_response(str(flask.request.json['dividend'] / flask.request.json['divider']), 200)
    res.content_type = 'text/plain'
    return res


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
