from flask import render_template, current_app, request
from markupsafe import Markup # Correct import for Markup
# from flask_login import login_required # Import later for security
from app.demand_admin import bp
from app.models import Recipient, Hub # Import models
import json # Import json for embedding data safely
# Remove imports not needed for basic map display for now
# import numpy as np
# from sklearn.cluster import KMeans
# from sklearn.exceptions import ConvergenceWarning
# import warnings
# import networkx as nx
# from geopy.distance import great_circle
# import os

# Remove helper functions for now
# def find_nearest_node(...)
# def load_graph(...)

@bp.route('/dashboard')
# @login_required # TODO: Add authentication check for QTV role
def dashboard():
    # """DEBUG: Renders a raw HTML page with the map directly, bypassing templates."""
    title = 'QTV Demand Dashboard'

    # Basic query for hubs
    try:
        hubs = Hub.query.filter(Hub.latitude.isnot(None), Hub.longitude.isnot(None)).all()
    except Exception as e:
        current_app.logger.error(f"Error querying hubs: {e}")
        hubs = []
    # Prepare hub data for JSON serialization (matching template script)
    hub_data = [ {
        'id': h.id, 
        'lat': h.latitude, 
        'lon': h.longitude, 
        'name': h.name, 
        'address': h.address # Added address for popup
        } 
        for h in hubs 
    ]
    # hub_data_json = json.dumps(hub_data) # No longer needed, pass directly to template

    # --- REMOVE Raw HTML String and return statement --- 
    # html_content = f""" ... """
    # return Markup(html_content)

    # --- ADD Render Template Call --- 
    return render_template(
        'demand_admin/dashboard.html', 
        title=title, 
        hubs=hub_data # Pass the list of hub dictionaries
        # TODO: Pass recipient data, cluster data, etc. later
    )

# Remove the separate planning_map route as it's integrated into the dashboard
# @bp.route('/planning-map')
# @login_required # TODO: Add authentication check for QTV role
# def planning_map():
#     """Renders the map interface for delivery planning."""
#     recipients = Recipient.query.filter(Recipient.latitude.isnot(None), Recipient.longitude.isnot(None)).all()
#     hubs = Hub.query.filter(Hub.latitude.isnot(None), Hub.longitude.isnot(None)).all()
#
#     # Prepare data in a JSON-serializable format for the template/JS
#     recipient_data = [
#         {'id': r.id, 'lat': r.latitude, 'lon': r.longitude, 'name': r.nickname or f'Recipient {r.id}'}
#         for r in recipients
#     ]
#     hub_data = [
#         {'id': h.id, 'lat': h.latitude, 'lon': h.longitude, 'name': h.name, 'type': h.hub_type.value}
#         for h in hubs
#     ]
#
#     return render_template(
#         'planning_map.html',
#         title='Bản đồ Lập kế hoạch Phân phối',
#         recipients=recipient_data, # Pass data as lists of dicts
#         hubs=hub_data
#     )

# Add other routes for specific functions (planning, tracking) later 