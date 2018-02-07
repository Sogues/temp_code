#!/usr/bin/env python
# encoding: utf-8

from work import FK, simple_template
from work.view import Controller
from core.base_view import BaseView
from work.log import LOG_FUNC_NAME, LOG_OUT

app = FK()

#@app.route('/index', methods=['GET'])
#def index():
#    return 'this is a test page'
#
#@app.route('/test/js')
#def test_js():
#    return '<script src="/static/test.js"></script>'
#
#@app.route('/')
#def hello():
#    return "hello page"

class Index(BaseView):
    @LOG_FUNC_NAME(class_name='Index')
    def get(self, request):
        return simple_template(
                'index.html',
                user='baidu_cloud',
                message='this is a test page')


class Test(Index):
    @LOG_FUNC_NAME(class_name='Test')
    def post(self, request):
        return "this is a Post request"


url_map = [
        {
            'url': '/index',
            'view': Index,
            'endpoint': 'index'
        },
        {
            'url': '/test',
            'view': Test,
            'endpoint': 'test'
        }
    ]

def main():
    print('-----app run !!!')
    index_controller = Controller('index', url_map)
    app.load_controller(index_controller)
    app.run()




if __name__ == '__main__':
    main()
