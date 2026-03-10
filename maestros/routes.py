from . import maestros

from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
import forms
from models import db, Maestros
from maestros.routes import maestros
from flask_migrate import Migrate

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route('/detallesM', methods=['GET','POST'])
def detalles():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        matricula = int(request.args.get("matricula"))
        #select * from maestros where matricula==matricula
        maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
        matricula=request.args.get('matricula')
        nombre=maes1.nombre
        apellidos=maes1.apellidos
        especialidad=maes1.especialidad
        email=maes1.email
        
        
    return render_template('maestros/detallesMaes.html', matricula=matricula,nombre=nombre,apellidos=apellidos,especialidad=especialidad,email=email,form=create_form)


@maestros.route('/modificarM', methods=['GET','POST'])
def modificar():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        matricula=request.args.get('matricula')
        # select * from maestros where matricula==matricula
        maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
        create_form.matricula.data=request.args.get('matricula')
        create_form.nombre.data=str.rstrip(maes1.nombre)
        create_form.apellidos.data=maes1.apellidos
        create_form.especialidad.data=maes1.especialidad
        create_form.email.data=maes1.email
        
    if request.method=='POST':
        matricula=create_form.matricula.data
        maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
        maes1.matricula=matricula
        maes1.nombre=str.rstrip(create_form.nombre.data)
        maes1.apellidos=create_form.apellidos.data
        maes1.especialidad=create_form.especialidad.data
        maes1.email=create_form.email.data
        
        db.session.add(maes1)
        db.session.commit()
        return redirect(url_for('maestros.listadoMaes'))
    return render_template('maestros/modificarMaes.html',form=create_form)

@maestros.route("/eliminarM", methods=['GET','POST'])
def eliminar():
    create_form=forms.UserForm(request.form)
    if request.method =='GET':
        matricula= request.args.get('matricula')
        maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
        if maes1:
            create_form.matricula.data=maes1.matricula
            create_form.nombre.data=maes1.nombre
            create_form.apellidos.data=maes1.apellidos
            create_form.especialidad.data=maes1.especialidad
            create_form.email.data=maes1.email
            
            return render_template("maestros/eliminarMaes.html", form=create_form)
        
    if request.method=='POST':
            matricula=create_form.matricula.data
            maes=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
            if maes:
                db.session.delete(maes)
                db.session.commit()
            return redirect(url_for('maestros.listadoMaes'))
    return render_template("maestros/eliminarMaes.html", form=create_form)


@maestros.route("/maestros", methods=['GET','POST'])
def maestro():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST' and create_form.validate():
        matricula = create_form.matricula.data
        existe = Maestros.query.filter_by(matricula=matricula).first()
        if existe:
            flash("⚠️ La matrícula ya está registrada", "warning")
            return render_template("maestros/maestros.html", form=create_form)
        try:
            maes = Maestros(
                matricula=matricula,
                nombre=create_form.nombre.data,
                apellidos=create_form.apellidos.data,
                especialidad=create_form.especialidad.data,
                email=create_form.email.data
            )
            db.session.add(maes)
            db.session.commit()
            flash("✅ Maestro registrado correctamente", "success")
            return redirect(url_for('maestros.listadoMaes'))
        except Exception as e:
            db.session.rollback()
            flash("❌ Error al guardar el maestro", "danger")

    return render_template("maestros/maestros.html", form=create_form)

@maestros.route("/listadoMaes")
def listadoMaes():
    create_form=forms.UserForm(request.form)
    #ORM select * from maestros
    maestro=Maestros.query.all()
    print("DATOS:", maestro)
    return render_template("maestros/listadoMaes.html",form=create_form, maestro=maestro)
