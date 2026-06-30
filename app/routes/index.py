from flask import (
    Blueprint, render_template, request, g, current_app
)

from ..validator import Validator, ValidateForm
from ..models import User
from ..repository import UserRepo
from ..services import UserService
from ..exceptions import UserExists

import json

index_blueprint = Blueprint('/', __name__, template_folder='templates')

@index_blueprint.route('/')
def index():

    dictr = {}

    with open("flores.json", "r") as f:
        dictr = json.load(f)

    return render_template('index.html', produtos=dictr)



@index_blueprint.route('/register', methods=("GET", "POST"))
def register():

    if request.method == 'GET':
        return render_template('register.html')

    if request.method == "POST":

        if (not request.form or request.content_type != ValidateForm.form_type):
            return "Bad Request", 400

        try:

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
                current_app.db
            )

            userRepo.register(user)

        except ValueError as e:
            return f"Bad request error: {e}", 400

        except UserExists as e:
            return f"Conflit.", 409

        return "post", 200


    return "", 400