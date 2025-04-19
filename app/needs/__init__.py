from flask import Blueprint

bp = Blueprint('needs', __name__, template_folder='templates')
 
from app.needs import routes, forms 