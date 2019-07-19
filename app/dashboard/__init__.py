from flask import Blueprint

dash_blueprint = Blueprint('dash', __name__)

from . import views