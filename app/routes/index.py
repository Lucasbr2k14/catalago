from flask import (
    Blueprint, render_template, request, g, current_app, redirect, url_for
)

from ..validator import Validator, ValidateForm
from ..models import User
from ..repository import UserRepo
from ..services import UserService
from ..exceptions import UserExists, InvalidUser
from ..decorators import login_required


import json

index_blueprint = Blueprint('/', __name__, template_folder='templates')

@index_blueprint.route('/')
def index():

    dictr = {}

    with open("flores.json", "r") as f:
        dictr = json.load(f)

    return render_template('index.html', produtos=dictr)


"""
TODO Refatorar toda a rota register para passar para tudo (o que for possivel) para services
"""
@index_blueprint.route('/register', methods=("GET", "POST"))
def register():

    if request.method == 'GET':
        return render_template('register.html')

    if request.method == "POST":

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


    return "", 400

"""
Por enquanto somente o token.
Mas é preciso fazer o refresh token para guardar a sessão do usuário.
É preciso nesse refresh token guardar o uuid da sessão.

refresh token = [
    uuid: str,
    timestamp: data
]

Com o refresh token é possivel criar uma rota para criar um token usando o jwt.

"""

@index_blueprint.route('/login', methods=("GET", "POST"))
def login():

    if request.method == "GET":
        return render_template("login.html"), 200

    if request.method == "POST":
        if (not request.form or request.content_type != ValidateForm.form_type):
            return "Bad Request", 400

        form = ValidateForm(
            request.form,
            {"email", "password"}
        )

        if not Validator.test_email(form["email"]):
            raise ValueError("Invalid email")

        app = current_app.extensions
        ur:UserRepo = UserRepo(app["db"])

        token = UserService.login(
            ur, 
            form["email"], 
            form["password"],
            app['configs'].jwt_secret,
            app['configs'].jwt_expire
        )
        
        response = redirect("/dashboard", code=303)

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure= not app['configs'].dev, #Mudar se desenvolvimento
            samesite="Lax",
            max_age=app['configs'].jwt_expire
        )

        return response, 303

    return "", 400


@index_blueprint.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user = g.user_token
    return render_template("dashboard.html", user=user), 200