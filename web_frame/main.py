#!/usr/bin/env python
# encoding: utf-8

from framework import FK

app = FK()

@app.route('/index', methods=['GET'])
def index():
    return 'this is a test page'

@app.route('/test/js')
def test_js():
    return '<script src="/static/test.js"></script>'

@app.route('/')
def hello():
    return "hello page"

def main():
    print('-----app run !!!')
    app.run()



if __name__ == '__main__':
    main()
