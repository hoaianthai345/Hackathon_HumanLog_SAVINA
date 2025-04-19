from flask import render_template, url_for, redirect
from app.main import bp

# Landing Page Route (Now at /landing)
@bp.route('/landing')
def landing():
    # Define roles similar to auth.select_role for display on landing page
    available_roles = [
        {
            'id': 'supply_inventory_admin',
            'name': 'QTV Supply & Inventory',
            'description': 'Quản lý nguồn cung và tồn kho.',
            'icon': 'bi-archive-fill',
            'url': url_for('supply_admin.dashboard') # Corrected URL
        },
        {
            'id': 'demand_distribution_admin',
            'name': 'QTV Demand & Distribution',
            'description': 'Quản lý nhu cầu và phân phối.',
            'icon': 'bi-truck',
            'url': url_for('demand_admin.dashboard') # Corrected URL
        },
        {
            'id': 'donor',
            'name': 'Nhà quyên góp',
            'description': 'Đăng ký và quản lý quyên góp.',
            'icon': 'bi-box2-heart-fill',
            'url': url_for('donations.register_donation') # Corrected URL from '#'
        },
        {
            'id': 'volunteer',
            'name': 'Tình nguyện viên',
            'description': 'Ghi nhận nhu cầu, vận chuyển.',
            'icon': 'bi-person-heart',
            'url': url_for('volunteer.dashboard') # Link to volunteer dashboard
        },
    ]
    # Pass roles to the template
    return render_template('landing_page.html', roles=available_roles)

# Dashboard Index Route (specific dashboard, potentially for admins)
@bp.route('/dashboard')
# @login_required # Add this later when auth is implemented
def dashboard_index():
    # Replace with actual data later
    # return render_template('dashboard_index.html', title='Bảng điều khiển') # Removed template render
    # Redirect to the landing page as dashboard_index.html is deleted
    return redirect(url_for('main.landing'))

# Superuser Dashboard Route (Now the main page at /)
@bp.route('/')
# @login_required # Add later & check for superuser role
def superuser_dashboard():
    # You can add logic here later to fetch summary data if needed
    return render_template('superuser_dashboard.html', title='Superuser Dashboard') 