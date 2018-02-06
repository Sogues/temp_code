from ..log import LOG_FUNC_NAME, LOG_OUT
class View:

    methods = None
    methods_meta = None

    @LOG_FUNC_NAME(class_name='View')
    def  dispatch_request(self, request, *args, **options):
        raise NotImplementedError

    @classmethod
    def get_func(cls, name):
        def func(*args, **kwargs):
            obj = func.view_class()
            return obj.dispatch_request(*args, **kwargs)
        func.view_class = cls
        func.__name__ = name
        func.__doc__ = cls.__doc__
        func.__module__ = cls.__module__
        func.methods = cls.methods
        return func


class Controller:

    @LOG_FUNC_NAME(class_name='Controller')
    def __init__(self, name, url_map):
        self.name = name
        self.url_map = url_map

    @LOG_FUNC_NAME(class_name='Controller')
    def __name__(self):
        return self.name
