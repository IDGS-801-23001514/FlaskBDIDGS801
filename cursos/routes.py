import forms
from . import curso
from flask import render_template, request, redirect, url_for, flash
from models import db, Curso, Maestros, Alumnos
from sqlalchemy.exc import IntegrityError


@curso.route("/cursos")
def index():
    cursos = Curso.query.all()
    return render_template("cursos/index.html", cursos=cursos)


@curso.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    form = forms.CursoForm(request.form)
    # cargar maestros en el select
    form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos}")
        for m in Maestros.query.all()
    ]
    if request.method == "POST" and form.validate():
        nuevo_curso = Curso(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            maestro_id=form.maestro_id.data
        )
        db.session.add(nuevo_curso)
        db.session.commit()
        return redirect(url_for("curso.index"))
    return render_template("cursos/nuevo.html", form=form)

@curso.route("/eliminarC", methods=['GET','POST'])
def eliminar():

    create_form = forms.CursoForm(request.form)
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos}")
        for m in Maestros.query.all()
    ]
    if request.method == 'GET':
        id = request.args.get('id')
        curs1 = db.session.query(Curso).filter(Curso.id == id).first()
        if curs1:
            create_form.id.data = curs1.id
            create_form.nombre.data = curs1.nombre
            create_form.descripcion.data = curs1.descripcion
            create_form.maestro_id.data = curs1.maestro_id

            return render_template("cursos/eliminarCur.html", form=create_form)
    if request.method == 'POST':
        id = create_form.id.data
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        if curso:
            db.session.delete(curso)
            db.session.commit()
        return redirect(url_for('curso.index'))
    return render_template("cursos/eliminarCur.html", form=create_form)

@curso.route("/inscribir/<int:curso_id>", methods=["GET", "POST"])
def inscribir(curso_id):
    curso_obj = Curso.query.get_or_404(curso_id)
    form = forms.InscripcionForm(request.form)

    form.alumno_id.choices = [
        (a.id, f"{a.nombre} {a.apellidos}")
        for a in Alumnos.query.all()
    ]

    if request.method == "POST" and form.validate():

        alumno = Alumnos.query.get(form.alumno_id.data)

        # 🔎 VALIDAR SI YA ESTÁ INSCRITO
        if alumno in curso_obj.alumnos:
            flash("⚠️ El alumno ya está inscrito en este curso", "warning")
            return redirect(url_for("curso.inscribir", curso_id=curso_id))

        try:
            curso_obj.alumnos.append(alumno)
            db.session.commit()
            flash("✅ Alumno inscrito correctamente", "success")

        except IntegrityError:
            db.session.rollback()
            flash("⚠️ El alumno ya está inscrito en este curso", "warning")

        return redirect(url_for("curso.inscribir", curso_id=curso_id))

    return render_template(
        "cursos/inscribir.html",
        form=form,
        curso=curso_obj
    )