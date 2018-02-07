from work.log import LOG_FUNC_NAME, LOG_OUT
import base64
import time


@LOG_FUNC_NAME()
def create_session_id():
    return base64.encodebytes(str(time.time()).encode()).decode().replace('=', '')[:-2][::-1]
