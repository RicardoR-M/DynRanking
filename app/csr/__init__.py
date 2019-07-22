from flask import Blueprint

csr_blueprint = Blueprint('csr', __name__)

from . import views