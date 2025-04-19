from flask import Blueprint

# Define the blueprint
# Use a template folder relative to the app's template folder
bp = Blueprint('supply_admin', __name__, template_folder='../templates/supply_admin', url_prefix='/supply-admin')

# Import routes after blueprint definition to avoid circular imports
from app.supply_admin import routes 