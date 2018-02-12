#!/usr/bin/env python
# encoding: utf-8

from work import FK, simple_template
from work.view import Controller
from core.base_view import BaseView, SessionView
from work.log import LOG_FUNC_NAME, LOG_OUT
from work.session import session

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

#class Index(BaseView):
#    @LOG_FUNC_NAME(class_name='Index')
#    def get(self, request):
#        return simple_template(
#                'index.html',
#                user='baidu_cloud',
#                message='this is a test page')
#
#
#class Test(Index):
#    @LOG_FUNC_NAME(class_name='Test')
#    def post(self, request):
#        return "this is a Post request"


class Index(SessionView):
    @LOG_FUNC_NAME(class_name='Index')
    def get(self, request):
        user = session.get(request, 'user')
        return simple_template('index.html', user=user, message='hello nico')


class Login(BaseView):
    @LOG_FUNC_NAME(class_name='Login')
    def get(self, request):
        return simple_template('login.html')

    @LOG_FUNC_NAME(class_name='Login')
    def post(self, request):
        user = request.form['user']

        session.push(request, 'user', user)
        return '登录成功, <a href="/">返回</a>'


class Logout(SessionView):
    @LOG_FUNC_NAME(class_name='Logout')
    def get(self, request):
        session.pop(request, 'user')
        return '登出成功, <a href='/'>返回</a>'


#url_map = [
#        {
#            'url': '/index',
#            'view': Index,
#            'endpoint': 'index'
#        },
#        {
#            'url': '/test',
#            'view': Test,
#            'endpoint': 'test'
#        }
#    ]

sys_url_map = [
        {
            'url': '/',
            'view': Index,
            'endpoint': 'index'
        },
        {
            'url': 'login',
            'view': Login,
            'endpoint': 'login'
        },
        {
            'url': '/logout',
            'view': Logout,
            'endpoint': 'logout'
        }
    ]

def main():
    print('-----app run !!!')
    index_controller = Controller('index', sys_url_map)
    app.load_controller(index_controller)
    app.run()




if __name__ == '__main__':
    main()
