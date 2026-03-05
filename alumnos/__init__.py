from flask import Blueprint

alumno=Blueprint(
    'alumno',
    __name__,
    template_folder='templates',
    static_folder='static')
from . import routes