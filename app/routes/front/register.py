from flask import request, render_template, current_app, redirect
from ...validator import ValidateForm, Validator
from ...repository import UserRepo
from ...services import UserService

from . import front

@front.get('/register')
def register_front():
    return render_template('register.html')

"""
TODO Refatorar toda a rota register para passar para tudo (o que for possivel) para services
"""
@front.post('/register')
def register():

    if (not request.form or request.content_type != ValidateForm.form_type):
        return "Bad Request", 400

    form = ValidateForm(
        request.form,
        {"name", "user_name", "email", "nascimento", "password"}
    )

    Validator.register_user(
        name       = form['name'],
        user_name  = form['user_name'],
        email      = form['email'],
        password   = form['password'],
        nascimento = form['nascimento']
    )

    user = UserService.register(
        name       = form['name'],
        user_name  = form['user_name'],
        email      = form['email'],
        password   = form['password'],
        nascimento = form['nascimento']
    )

    userRepo = UserRepo(
        current_app.extensions["db"]
    )

    userRepo.register(user)

    return redirect("/login")
