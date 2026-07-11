from functools import wraps
from flask import g, request, redirect, current_app
from ..services import SegurityService
from ..exceptions import AuthenticationError


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("access_token")

        if not token:
            raise AuthenticationError()
        
        g.user_token = SegurityService.validate_jwt(token)

        return func(*args, **kwargs)
    
    return wrapper