from flask import Blueprint

# Define the blueprint
bp = Blueprint('demand_admin', __name__, template_folder='../templates/demand_admin', url_prefix='/demand-admin')

# Import routes after blueprint definition
from app.demand_admin import routes 