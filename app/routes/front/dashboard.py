from flask import render_template, g, request
from ...decorators import login_required

from . import front

@front.get("/dashboard")
@login_required
def dashboard():
    if request.method == "GET":
        user = g.user_token

        return render_template("dashboard.html", user=user, login=True), 200
    
    return "", 405