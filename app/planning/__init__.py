from flask import Blueprint

bp = Blueprint('planning', __name__, template_folder='templates')
 
from app.planning import routes, services 