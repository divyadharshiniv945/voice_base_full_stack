from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return view_function(*args, **kwargs)

    return wrapper


def active_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_active:
            abort(403)
        return view_function(*args, **kwargs)

    return wrapper
