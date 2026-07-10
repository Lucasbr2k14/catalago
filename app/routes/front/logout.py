from flask import request, redirect

from . import front 

@front.post("/logout")
def logout():
    response = redirect("/login", code=303)
    response.delete_cookie("access_token")
    return response