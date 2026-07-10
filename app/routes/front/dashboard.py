from flask import render_template, g, request
from ...decorators import login_required

from . import front


@front.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if request.method == "GET":
        user = g.user_token
        return render_template("dashboard.html", user=user), 200
    
    return "", 405