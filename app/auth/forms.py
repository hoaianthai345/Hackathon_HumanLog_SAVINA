# Auth forms go here 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Ghi nhớ tôi')
    submit = SubmitField('Đăng nhập')

# Add RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm later if needed 