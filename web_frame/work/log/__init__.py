# encoding: utf-8

import logging
logging.basicConfig(
        level=logging.INFO
       )
logger = logging.getLogger(__name__)

def LOG_FUNC_NAME(**dkargs):
    def wrapper(func):
        log_func = dkargs.get('log_func', logger.info)
        class_name = dkargs.get('class_name',None)
        def _wrapper(*args, **kwargs):
            if class_name:
                log_func('  '+class_name+'::{}'.format(func.__name__))
            else:
                log_func('  {}'.format(func.__name__))
            return func(*args, **kwargs)
        return _wrapper
    return wrapper



def LOG_OUT(_log, *args):
    log_func = None
    if _log == 'info':
        log_func = logger.info
    elif _log == 'debug':
        log_func = logger.debug
    elif _log == 'warning':
        log_func = logger.warning
    else:
        log_func = logger.error
    log_func(*args);

