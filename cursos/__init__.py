from flask import Blueprint

curso = Blueprint(
    "curso",
    __name__,
    template_folder="templates",
    static_folder="static"
)

from . import routes