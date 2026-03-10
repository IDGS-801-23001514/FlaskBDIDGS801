from wtforms import Form, HiddenField
from wtforms import StringField, IntegerField,PasswordField,FloatField, BooleanField,SelectField,TextAreaField
from wtforms import EmailField
from wtforms import validators


class UserForm2(Form):
    id=IntegerField("id",
                    [validators.number_range(min=1, max=20,message="valor no valido")])
    nombre=StringField("nombre",[
        validators.DataRequired(message="El nombre es requerido"),
        validators.length(min=4,max=20,message="requiere min =4 y max = 20")
    ])
    apellidos=StringField("apellidos",[
        validators.DataRequired(message="Los apellidos son requeridos")
    ])
    email=EmailField("correo",[
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo valido")
    ])
    telefono=StringField("telefono",[
        validators.DataRequired(message="El telefono es requerido"),
        validators.DataRequired(message="Ingrese un telefono valido")
    ])
    
    
class UserForm(Form):
    matricula = IntegerField("matricula", [
    validators.DataRequired(message="La matrícula es requerida")
    ])
    nombre=StringField("nombre",[
        validators.DataRequired(message="El nombre es requerido"),
        validators.length(min=4,max=20,message="requiere min =4 y max = 20")
    ])
    apellidos=StringField("apellidos",[
        validators.DataRequired(message="Los apellidos son requeridos")
    ])
    especialidad=StringField("especialidad",[
        validators.DataRequired(message="La especialidad es requerida")
    ])
    email=EmailField("correo",[
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo valido")
    ])
    
class CursoForm(Form):
    id = HiddenField()
    nombre = StringField("Nombre del Curso", [
        validators.DataRequired(message="El nombre es obligatorio")
    ])

    descripcion = TextAreaField("Descripción")

    maestro_id = SelectField(
        "Maestro",
        coerce=int,
        validators=[validators.DataRequired(message="Seleccione un maestro")]
    )


class InscripcionForm(Form):
    alumno_id = SelectField(
        "Alumno",
        coerce=int,
        validators=[validators.DataRequired(message="Seleccione un alumno")]
    )