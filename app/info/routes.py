from flask import render_template
from app.info import bp

@bp.route('/about')
def about():
    return render_template('info/about.html', title='Về chúng tôi')

@bp.route('/guest')
def guest():
    return render_template('info/guest.html', title='Thông tin Khách')

@bp.route('/donation-registration-info')
def donation_registration_info():
    return render_template('info/donation_registration_info.html', title='Đăng ký quyên góp')