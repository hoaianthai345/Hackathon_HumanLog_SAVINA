from flask import render_template
# from flask_login import login_required # Import later for security
from sqlalchemy import func # Import func for SUM
from app import db # Import db instance
from app.models import Donation, DonationStatus # Import models
from app.supply_admin import bp

@bp.route('/dashboard')
# @login_required # TODO: Add authentication check for QTV role
def dashboard():
    """Renders the main dashboard for Supply & Inventory QTVs."""

    # Query total available quantity per category
    category_totals_query = db.session.query(
        Donation.category,
        func.sum(Donation.quantity).label('total_quantity')
    ).filter(
        Donation.status == DonationStatus.AVAILABLE
    ).group_by(
        Donation.category
    ).order_by(
        Donation.category
    )

    category_totals = {row.category: int(row.total_quantity) for row in category_totals_query.all()}

    # Calculate overall total
    overall_total = sum(category_totals.values())

    return render_template(
        'dashboard.html',
        title='QTV - Quản lý Kho & Cung ứng',
        category_totals=category_totals,
        overall_total=overall_total
    )

# Add other routes for specific functions later (e.g., reports, alerts, etc.) 