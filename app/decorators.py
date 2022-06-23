from functools import wraps

from flask import make_response

def cache_control(minutes=10):
    """Returns a Flask decorator that sets Cache-Control header. """
    def decorator(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            r = func(*args, **kwargs)
            rsp = make_response(r, 200)
            rsp.headers.add('Cache-Control', 'public,max-age=%d' % int(3600 * 60 * minutes))
            return rsp
        return decorated_func
    return decorator
