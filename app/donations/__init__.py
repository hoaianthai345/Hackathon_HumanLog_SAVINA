from flask import Blueprint

bp = Blueprint('donations', __name__, template_folder='templates')
 
from app.donations import routes, forms 