from flask import Blueprint

bp = Blueprint('tracking', __name__, template_folder='templates')
 
from app.tracking import routes 