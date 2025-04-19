# Auth routes go here 
from flask import render_template, flash, redirect, url_for, request
from app.auth import bp
from app.auth.forms import LoginForm
# from flask_login import current_user, login_user, logout_user # Import later
# from app.models import User # Import later
# from werkzeug.urls import url_parse # Import later

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated: # Add later
    #     return redirect(url_for('main.dashboard_index'))
    form = LoginForm()
    if form.validate_on_submit():
        # --- Placeholder Login Logic ---
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is None or not user.check_password(form.password.data):
        #     flash('Email hoặc mật khẩu không hợp lệ')
        #     return redirect(url_for('auth.login'))
        # login_user(user, remember=form.remember_me.data)
        # --- End Placeholder ---

        flash('Đăng nhập thành công!') # Temporary flash message
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('auth.select_role') # Redirect to role selection
        # return redirect(next_page)
        return redirect(url_for('auth.select_role')) # Redirect to role selection for now

    return render_template('auth/login.html', title='Đăng nhập', form=form)

@bp.route('/logout')
def logout():
    # logout_user() # Add later
    flash('Bạn đã đăng xuất.')
    return redirect(url_for('main.landing'))

# @login_required # Add later
@bp.route('/select-role')
def select_role():
    # In a real app, you might fetch available roles for the logged-in user
    # For now, we define static roles based on the new requirement
    available_roles = [
        {
            'id': 'supply_inventory_admin',
            'name': 'QTV Supply & Inventory', # Shortened name for box
            'description': 'Quản lý nguồn cung và tồn kho.',
            'icon': 'bi-archive-fill', # Icon for inventory/supply
            'url': url_for('main.dashboard_index') # Link to general dashboard for now
        },
        {
            'id': 'demand_distribution_admin',
            'name': 'QTV Demand & Distribution',
            'description': 'Quản lý nhu cầu và phân phối.',
            'icon': 'bi-truck', # Icon for distribution
            'url': url_for('main.dashboard_index') # Link to general dashboard for now
        },
        {
            'id': 'donor',
            'name': 'Nhà quyên góp',
            'description': 'Đăng ký và quản lý quyên góp.',
            'icon': 'bi-box2-heart-fill',
            'url': '#' # Placeholder URL - Needs dedicated donor dashboard/page
        },
        {
            'id': 'volunteer',
            'name': 'Tình nguyện viên',
            'description': 'Ghi nhận nhu cầu, vận chuyển.',
            'icon': 'bi-person-heart',
            'url': url_for('volunteer.dashboard') # Updated URL
        },
    ]
    return render_template('auth/select_role.html', title='Chọn vai trò', roles=available_roles)

# Add registration, password reset routes later 