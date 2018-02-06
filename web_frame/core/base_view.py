#!/usr/bin/env python
# encoding: utf-8

from work.view import View
from work.log import LOG_FUNC_NAME, LOG_OUT

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
