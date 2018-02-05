from werkzeug.wrappers import Request

def wsgi_app(app, environ, start_response):
    """
    app: 应用
    environ: 服务器传过来的请求
    start_response: 响应载体，不会使用，连同处理结果一起传回给服务器
    """
    request = Request(environ)
    response = app.dispatch_request(request)
    return response(environ, start_response)
