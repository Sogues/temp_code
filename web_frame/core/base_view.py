#!/usr/bin/env python
# encoding: utf-8

from work.view import View
from work.log import LOG_FUNC_NAME, LOG_OUT
from work.session import AuthSession, session

class BaseView(View):

    methods = ['GET', 'POST']

    @LOG_FUNC_NAME(class_name='BaseView')
    def post(self, request, *args, **options):
        pass

    @LOG_FUNC_NAME(class_name='BaseView')
    def get(self, request, *args, **options):
        pass

    @LOG_FUNC_NAME(class_name='BaseView')
    def dispatch_request(self, request, *args, **options):
        methods_meta = {
                'GET': self.get,
                'POST': self.post
                }
        if request.method in methods_meta:
            return methods_meta[request.method](request, *args, **options)
        else:
            return '<h1>Unknown or unsupported require method</h1>'


class AuthLogin(AuthSession):

    @staticmethod
    def auth_fail_callback(request, *args, **options):
        return '<a href="/login">登录</a>'

    @staticmethod
    def auth_logic(request, *args, **options):
        if 'user' in session.map(request).keys():
            return True
        return False


class SessionView(BaseView):

    @AuthLogin.auth_session
    def dispatch_request(self, requtest, *args, **options):
        return super(SessionView, self).dispatch_request(request, *args, **options)
