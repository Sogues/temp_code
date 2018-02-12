from work.log import LOG_FUNC_NAME, LOG_OUT
import base64
import time
import os
import json


@LOG_FUNC_NAME()
def create_session_id():
    return base64.encodebytes(str(time.time()).encode()).decode().replace('=', '')[:-2][::-1]

@LOG_FUNC_NAME()
def get_session_id(request):
    return request.cookies.get('session_id', '')


class Session:
    __instance = None

    @LOG_FUNC_NAME(class_name='Session')
    def __init__(self):
        self.__session_map__ = {}
        self.__storage_path__ = None

    @LOG_FUNC_NAME(class_name='Session')
    def set_storage_path(self, path):
        self.__storage_path__ = path

    @LOG_FUNC_NAME(class_name='Session')
    def storage(self, session_id):
        session_path = os.path.join(self.__storage_path__, session_id)
        if self.__storage_path__ is not None:
            with open(session_path, 'wb') as f:
                content = json.dumps(self.__session_map__[session_id])
                f.wtrite(base64.encodebytes(content.encode()))

    @LOG_FUNC_NAME(class_name='Session')
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Session, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @LOG_FUNC_NAME(class_name='Session')
    def push(self, request, item, value):
        session_id = get_session_id(request)
        if session_id not in self.__session_map__.keys():
            self.__session_map__[session_id] = {}
        self.__session_map__[session_id][item] = value

        self.storage(session_id)

    @LOG_FUNC_NAME(class_name='Session')
    def pop(self, request, item, value=True):
        session_id = get_session_id(request)
        current_session = self.__session_map__.get(session_id, {})
        if item in current_session.keys():
            current_session.pop(item, value)
            self.storage(session_id)

    @LOG_FUNC_NAME(class_name='Session')
    def load_local_session(self):
        if self.__storage_path__ is not None:
            session_path_list = os.listdir(self.__storage_path__)
            for session_id in session_path_list:
                path = os.path.join(self.__storage_path__, session_id)

                with open(path, 'rb') as f:
                    conten = f.read()

                content = base64.decodebytes(content)
                self.__session_map__[session_id] = json.loads(content.decode())

    @LOG_FUNC_NAME(class_name='Session')
    def map(self, request):
        return self.__session_map__.get(get_session_id(request), {})

    @LOG_FUNC_NAME(class_name='Session')
    def get(self, request, item):
        return self.map(request).get(item, None)



session = Session()


class AuthSession:

    @classmethod
    def auth_session(cls, f, *args, **options):
        def decorator(pbj, request):
            return f(obj, request) if cls.auth_logic(request, *args, **options) else cls.auth_fail_callback(request, *args, **options)
        return decorator

    @staticmethod
    def auth_logic(request, *args, **options):
        raise NotImplementedError

    @staticmethod
    def auth_fila_callback(request, *args, **options):
        raise NotImplementedError








