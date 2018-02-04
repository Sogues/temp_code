#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'hello world'

@app.route('/')
def index():
    return 'Index page'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User {}'.format(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post {}'.format(post_id)

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/list')
def do_ls():
    try:
        import os
        os.system('ls -alh')
    except Exception as ex:
        return ex
    return 'list Success'

@app.route('/sum/<a>/<b>')
def app_sum(a, b):
    try:
        ans = float(a) + float(b)
        return '{} + {} = {}'.format(a, b, ans)
    except Exception as ex:
        return ex

if __name__ == '__main__':
    app.run(host='0.0.0.0')
