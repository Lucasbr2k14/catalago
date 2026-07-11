from .exceptions import *
from flask import Flask, render_template, redirect



def register_errors(app:Flask):

    @app.errorhandler(UserExists)
    def userExists(err):
        return ("User already registered.", 409)

    @app.errorhandler(InvalidUser)
    def invadUser(err):
        return (f"Invalid user: {err}", 400)

    @app.errorhandler(ValueError)
    def valueErr(e):
        return (f"Bad request: {e}", 400)
    
    @app.errorhandler(TokenInvalid)
    def tokenInvalid(e):
        return redirect("/login")
    
    @app.errorhandler(TokenExpired)
    def tokenExpired(e):
        return redirect("/login")
    
    @app.errorhandler(InternalErr)
    def InternalError(e):
        return "Internal error.", 500

    @app.errorhandler(AuthorizationError)
    def Authorization(e):
        return f"Authorization error.", 401

    @app.errorhandler(AuthenticationError)
    def Authentication(e):
        return "Authentication error", 401

    @app.errorhandler(404)
    def notFoundError(e):
        return render_template("erros/notfound.html"), 404
    
    @app.errorhandler(400)
    def badRequest(e):
        return "Bad request", 400
    
    @app.errorhandler(ProductExists)
    def prodExists(e):
        return "Product exists", 409