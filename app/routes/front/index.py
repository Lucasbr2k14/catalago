from flask import render_template

import json

from . import front

@front.route('/')
def index():

    dictr = {}

    with open("flores.json", "r") as f:
        dictr = json.load(f)

    return render_template('index.html', produtos=dictr, login=True)
