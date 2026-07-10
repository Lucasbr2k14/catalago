from flask import request, render_template, redirect, current_app
from ...validator import ValidateForm, Validator
from ...repository import UserRepo
from ...services import UserService

from . import front


@front.get('/login')
def login_front():
    if request.method == "GET":
        token = request.cookies.get("access_token")

    if token:
        return redirect("/dashboard"), 303

    return render_template("login.html"), 200


@front.post('/login')
def login():

    if (not request.form or request.content_type != ValidateForm.form_type):
        return "Bad Request", 400

    form = ValidateForm(
        request.form,
        {"email", "password"}
    )

    if not Validator.test_email(form["email"]):
        raise ValueError("Invalid email")

    app = current_app.extensions

    ur:UserRepo = UserRepo( app['db'] )

    token = UserService.login(
        ur, 
        form["email"], 
        form["password"],
    )
    
    response = redirect("/dashboard")

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure= not app['configs'].dev, #Mudar se desenvolvimento
        samesite="Lax",
        max_age=app['configs'].jwt_expire
    )

    return response, 303
