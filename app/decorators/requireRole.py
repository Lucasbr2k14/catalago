from functools import wraps
from flask import g, request, redirect, current_app
from ..exceptions import AuthorizationError

def require_role(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*arg, **kwargs):
            if not g.user_token['role'] in roles or not g.user_token['role']:
                raise AuthorizationError()

            return func(*arg, **kwargs)
        
        return wrapper
    
    return decorator