from flask import Flask, render_template
import json



app = Flask(
    __name__
)

@app.route("/")
def index():
    produtos:list | None = None 

    with open('flores.json', 'r') as f:
        produtos = json.load(f)
        
    return render_template("index.html", produtos=produtos)