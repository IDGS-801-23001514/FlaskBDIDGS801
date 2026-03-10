from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
import forms
from models import db, Alumnos, Maestros, Curso, Inscripcion
from maestros.routes import maestros
from alumnos.routes import alumno
from cursos.routes import curso
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros)#registra el blueprint de maestros
app.register_blueprint(alumno)#registra el blueprint de alumnos
app.register_blueprint(curso)#registra el blueprint de cursos
csrf=CSRFProtect()
db.init_app(app)
migrate=Migrate(app,db)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404

@app.route("/")
def inicio():
    return render_template("inicio.html")

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
app.run()
