import forms
from . import alumno

from flask import Flask, render_template, request, redirect, url_for
from models import db, Alumnos

@alumno.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@alumno.route("/alumnos", methods=['GET','POST'])
def alumnos():
    create_form=forms.UserForm2(request.form)
    if request.method=='POST':
        alum=Alumnos(nombre=create_form.nombre.data,
                     apellidos=create_form.apellidos.data,
                     email=create_form.email.data,
                     telefono=create_form.telefono.data)
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumno.index'))
    return render_template("alumnos/alumnos.html", form=create_form)

@alumno.route('/detalles', methods=['GET','POST'])
def detalles():
    create_form=forms.UserForm2(request.form)
    if request.method=='GET':
        id = int(request.args.get("id"))
        #select * from alumnos where id==id
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        id=request.args.get('id')
        nombre=alum1.nombre
        apellidos=alum1.apellidos
        email=alum1.email
        telefono=alum1.telefono
        
    return render_template('alumnos/detalles.html', id=id,nombre=nombre,apellidos=apellidos,email=email,telefono=telefono,form=create_form)

@alumno.route('/modificar', methods=['GET','POST'])
def modificar():
    create_form=forms.UserForm2(request.form)
    if request.method=='GET':
        id=int(request.args.get('id'))
        # select * from alumnos where id==id
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=str.rstrip(alum1.nombre)
        create_form.apellidos.data=alum1.apellidos
        create_form.email.data=alum1.email
        create_form.telefono.data=alum1.telefono
    if request.method=='POST':
        id=create_form.id.data
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum1.id=id
        alum1.nombre=str.rstrip(create_form.nombre.data)
        alum1.apellidos=create_form.apellidos.data
        alum1.email=create_form.email.data
        alum1.telefono=create_form.telefono.data
        db.session.add(alum1)
        db.session.commit()
        return redirect(url_for('alumno.index'))
    return render_template('alumnos/modificar.html',form=create_form)

@alumno.route("/eliminar", methods=['GET','POST'])
def eliminar():
    create_form=forms.UserForm2(request.form)
    if request.method =='GET':
        id= request.args.get('id')
        alumn1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        if alumn1:
            create_form.id.data=alumn1.id
            create_form.nombre.data=alumn1.nombre
            create_form.apellidos.data=alumn1.apellidos
            create_form.email.data=alumn1.email
            create_form.telefono.data=alumn1.telefono
            return render_template("alumnos/eliminar.html", form=create_form)
        
    if request.method=='POST':
            id=create_form.id.data
            alumn=db.session.query(Alumnos).filter(Alumnos.id==id).first()
            if alumn:
                db.session.delete(alumn)
                db.session.commit()
            return redirect(url_for('alumno.index'))
    return render_template("alumnos/eliminar.html", form=create_form)


@alumno.route("/index")
def index():
    create_form=forms.UserForm2(request.form)
    #ORM select * from alumnos
    alumno=Alumnos.query.all()
    return render_template("alumnos/index.html",form=create_form, alumno=alumno)
