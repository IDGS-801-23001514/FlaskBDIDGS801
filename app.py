from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
import forms
from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")


if __name__ == '__main__':
	app.run(debug=True)
