from flask import render_template, flash, redirect, url_for, request
from sqlalchemy import desc # Import desc for ordering
# from flask_login import login_required, current_user # Import later
from app import db
from app.volunteer import bp
from app.volunteer.forms import RecipientForm
from app.models import Recipient, Hub, HubType, Delivery, DeliveryStatus, Volunteer, VolunteerReport, RouteStatus, RecipientType

# Placeholder for getting the current volunteer (replace with Flask-Login)
# def get_current_volunteer():
#     # In a real app, use current_user from Flask-Login
#     # return current_user.volunteer_profile
#     # For testing, assume volunteer with ID 1 exists
#     # return Volunteer.query.get(1) # Commented out for testing dashboard directly

@bp.route('/')
@bp.route('/dashboard')
# @login_required # Add later
def dashboard():
    # Bypass volunteer check for testing
    # volunteer = get_current_volunteer()
    # if not volunteer:
    #     flash('Không tìm thấy hồ sơ tình nguyện viên (ID=1).')
    #     return redirect(url_for('main.landing'))

    # Provide placeholder data for testing
    volunteer_data = {
        'name': 'Test Volunteer',
        'id': 999,
        'rating': 4.5,
        'volunteer_role': 'Driver', # Example role
        'area': 'District 1' # Example area
        # Add other fields as needed by the template
    }

    # Placeholder for tasks and activity
    assigned_tasks = [] # No assigned tasks for now
    recent_activity = [] # No recent activity for now

    # Placeholder for gamification
    gamification_data = {
        'rating': 0, # Default rating
        'task_count': 0 # Default task count
        # Add logic for badges/levels later if needed for template rendering
    }

    return render_template(
        'volunteer/dashboard.html',
        title='Bảng điều khiển TNV',
        volunteer=volunteer_data, # Use placeholder data object/dict
        assigned_tasks=assigned_tasks,
        recent_activity=recent_activity,
        gamification=gamification_data
    )

@bp.route('/add_recipient', methods=['GET', 'POST'])
# @login_required # Add later
def add_recipient():
    # Bypass volunteer check for testing
    # volunteer = get_current_volunteer()
    # if not volunteer:
    #     flash('Không tìm thấy hồ sơ tình nguyện viên.')
    #     return redirect(url_for('auth.login')) # Redirect to login if needed later

    form = RecipientForm()
    if form.validate_on_submit():
        lat_str = form.latitude.data
        lon_str = form.longitude.data
        latitude = None
        longitude = None

        # Validate and convert coordinates
        try:
            # Check if strings are non-empty before converting
            if lat_str and lon_str:
                latitude = float(lat_str)
                longitude = float(lon_str)
            else:
                # If either is empty, flash error and re-render
                flash('Vui lòng chọn một vị trí trên bản đồ hoặc lấy vị trí hiện tại.')
                # Optionally add error to a visible field like address?
                # form.address.errors.append('Vui lòng chọn vị trí trên bản đồ.') 
                return render_template('volunteer/add_recipient.html', title='Thêm người nhận', form=form)
        except ValueError:
            # Handle case where data is not a valid float (shouldn't happen with hidden fields, but good practice)
            flash('Dữ liệu Vĩ độ/Kinh độ không hợp lệ.')
            return render_template('volunteer/add_recipient.html', title='Thêm người nhận', form=form)

        # Proceed only if coordinates are valid
        recipient = Recipient(
            nickname=form.nickname.data,
            address=form.address.data, # Make sure address is also saved if needed
            latitude=latitude,
            longitude=longitude,
            has_kitchen=form.has_kitchen.data,
            recipient_type=RecipientType(form.recipient_type.data),
            note=form.note.data
        )
        db.session.add(recipient)
        db.session.commit()
        # Optionally, create a VolunteerReport here
        # report = VolunteerReport(volunteer_id=volunteer.id, recipient_id=recipient.id, notes=f"Recipient added by {volunteer.name}")
        # db.session.add(report)
        # db.session.commit()
        flash(f'Đã thêm người nhận: {recipient.nickname}')
        return redirect(url_for('volunteer.dashboard'))

    # Render form for GET request or if validation fails
    return render_template('volunteer/add_recipient.html', title='Thêm người nhận', form=form)

# Add route for marking delivery as delivered/failed later 