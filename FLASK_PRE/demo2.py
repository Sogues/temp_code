#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask import render_template, make_response, abort
from flask import request

app = Flask(__name__)

@app.route('/user/<username>')
def user_index(username):
    if username == 'invalid':
        abort(404)
    resp = make_response(render_template('user_index.html', username=username))
    print('---:', resp)
    resp.set_cookie('username', username)
    print('---:', resp)
    return resp

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
