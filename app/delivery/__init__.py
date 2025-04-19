from flask import Blueprint

bp = Blueprint('delivery', __name__, template_folder='templates')
 
from app.delivery import routes, forms 