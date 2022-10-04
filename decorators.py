from flask import g, redirect, url_for
from functools import wraps


def login_required(func):
    # when url_for is called, usually, for example, url_for('user.login')
    # login func will be called, however, due to the login_required func, login func can not be found
    # it can only find the returned func wrapper
    # Thus, in order to make 'login' func findable, do remember to add a @wraps(func) before your write the wrapper
    @wraps(func)
    def wrapper(*args, **kargs):
        if hasattr(g, 'user'):
            return func(*args, **kargs)
        else:
            return redirect(url_for('user.login'))

    return wrapper
