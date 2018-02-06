from work.log import LOG_FUNC_NAME, LOG_OUT

class Route:
    @LOG_FUNC_NAME(class_name='Route')
    def __init__(self, app):
        self.app = app

    @LOG_FUNC_NAME(class_name='Route')
    def __call__(self, url, **options):
        _str = ""
        for key, value in options.items():
            _str += str(key) + ': ' + str(value)

        if _str != "":
            LOG_OUT('debug', _str)

        if 'methods' not in options:
            options['methods'] = ['GET']
        def decorator(f):
            self.app.add_url_rule(url, f, 'route', **options)
            return f
        return decorator
