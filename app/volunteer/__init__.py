from flask import Blueprint

bp = Blueprint('volunteer', __name__, template_folder='templates', url_prefix='/volunteer')

# Import routes and forms after blueprint creation
from app.volunteer import routes, forms 