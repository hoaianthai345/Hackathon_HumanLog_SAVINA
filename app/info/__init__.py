from flask import Blueprint

bp = Blueprint('info', __name__, template_folder='templates', url_prefix='/tham-khao')

from app.info import routes 