#!/usr/bin/env python
# encoding: utf-8

from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from work.wsgi_adapter import wsgi_app
import work.exceptions as exceptions
from work.helper import parse_static_key
from work.route import Route
from work.log import LOG_FUNC_NAME, LOG_OUT

import os

class ExecFunc:
    @LOG_FUNC_NAME(class_name='ExecFunc')
    def __init__(self, func, func_type, **options):
        self.func = func
        self.options = options
        self.func_type = func_type

ERROR_MAP = {
    '401': Response('<h1>401 Unknown or unsupported method</h1>', content_type='text/html; charset=UTF-8', status=401),
    '404': Response('<h1>404 Source Not Found<h1>', content_type='text/html; charset=UTF-8', status=404),
    '503': Response('<h1>503 Unknown function type</h1>', content_type='text/html; charset=UTF-8',  status=503)
}

# 定义文件类型
TYPE_MAP = {
    'css':  'text/css',
    'js': 'text/js',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg'
}

class FK:
    @LOG_FUNC_NAME(class_name='FK')
    def __init__(self, static_folder='static'):
        self.host = '0.0.0.0'
        self.port = 5000
        self.url_map = {}
        self.static_map = {}
        self.function_map = {}
        self.static_folder = static_folder
        self.route = Route(self)

    @LOG_FUNC_NAME(class_name='FK')
    def dispatch_request(self, request):
        LOG_OUT('info', '  request.url: {}, methods: {}'.
                format(request.url, request.method))
        url = '/' + '/'.join(request.url.split('/')[3:]).split('?')[0]
        LOG_OUT('info', '  url: {}'.format(url))
        if (url.find(self.static_folder) == 1 and
                url.index(self.static_folder) == 1):
            endpoint = 'static'
            url = url[1:]
        else:
            endpoint = self.url_map.get(url, None)


        headers = {
                'Server': 'WEB Framework 0.1'
                }

        if endpoint is None:
            return ERROR_MAP['404']

        LOG_OUT('info', "  dispatch_request endpoint:{}".format(endpoint))


        exec_function = self.function_map[endpoint]

        LOG_OUT('info', "  func_type:{} methods:{}".
                format(exec_function.func_type, exec_function.options.get('methods')))

        if exec_function.func_type == 'route':
            if request.method in exec_function.options.get('methods'):
                argcount = exec_function.func.__code__.co_argcount

                if argcount > 0:
                    rep = exec_function.func(request)
                else:
                    rep = exec_function.func()
            else:
                return ERROR_MAP['401']
        elif exec_function.func_type == 'view':
            rep = exec_function.func(request)
        elif exec_function.func_type == 'static':
            return exec_function.func(url)
        else:
            return ERROR_MAP['503']

        status = 200
        content_type = 'text/html'

        return Response(
                rep,
                content_type='%s; charset=UTF-8' % content_type,
                headers=headers,
                status=status)
        """
        return Response(
                '<h1>Hello work</h1>',
                content_type='text/html',
                headers=headers,
                status=status)
        """

    @LOG_FUNC_NAME(class_name='FK')
    def run(self, host=None, port=None, **options):
        for key, value in options.items():
            if value is not None:
                self.__setattr__(key, value)

        if host:
            self.host = host

        if port:
            self.port = port

        self.function_map['static'] = ExecFunc(
                func=self.dispatch_static,
                func_type='static')

        run_simple(hostname=self.host, port=self.port, application=self, **options)

    @LOG_FUNC_NAME(class_name='FK')
    def __call__(self, environ, start_response):
        print('-----')
        print('environ:', environ)
        print('start_response', start_response)
        print('-----')
        return wsgi_app(self, environ, start_response)

    @LOG_FUNC_NAME(class_name='FK')
    def add_url_rule(self, url, func, func_type, endpoint=None, **options):
        if endpoint is None:
            endpoint = func.__name__
        else:
            LOG_OUT('info', "  {} {}".format(self.__class__.__name__, endpoint))

        if url in self.url_map:
            raise exceptions.URLExistsError

        if endpoint in self.function_map and func_type != 'static':
            raise exceptions.EndpointExistsError

        self.url_map[url] = endpoint
        self.function_map[endpoint] = ExecFunc(func, func_type, **options)

    @LOG_FUNC_NAME(class_name='FK')
    def bind_view(self, url, view_class, endpoint):
        LOG_OUT('info', '  bind_view endpoint: {}'.format(endpoint))
        self.add_url_rule(url, func=view_class.get_func(endpoint), func_type='view')

    @LOG_FUNC_NAME(class_name='FK')
    def load_controller(self, controller):
        name = controller.__name__()
        for rule in controller.url_map:
            LOG_OUT('info', '  rule: {}'.format(rule))
            self.bind_view(
                    rule['url'],
                    rule['view'],
                    name+'.'+rule['endpoint'])

    @LOG_FUNC_NAME(class_name='FK')
    def dispatch_static(self, static_path):
        if os.path.exists(static_path):
            key = parse_static_key(static_path)
            doc_type = TYPE_MAP.get(key, 'text/plain')
            with open(static_path, 'rb') as f:
                rep = f.read()
            return Response(rep, content_type=doc_type)
        else:
            return ERROR_MAP['404']
