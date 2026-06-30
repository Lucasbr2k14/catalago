from .exceptions import *
from flask import Flask, render_template, redirect



def register_errors(app:Flask):

    @app.errorhandler(UserExists)
    def userExists(err):
        return ("User already registered.", 409)


    @app.errorhandler(InvalidUser)
    def invadUser(err):
        return ("Invalid user", 400)


    @app.errorhandler(ValueError)
    def valueErr(e):
        return (f"Bad request: {e}", 400)
    

    @app.errorhandler(TokenInvalid)
    def tokenInvalid(e):
        return redirect("/login")
    
    
    @app.errorhandler(TokenExpired)
    def tokenExpired(e):
        return redirect("/login")
    

    @app.errorhandler(404)
    def notFoundError(e):
        return render_template("erros/notfound.html"), 404
    