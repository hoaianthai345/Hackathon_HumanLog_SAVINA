from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, BooleanField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from app.models import RecipientType # Import the Enum

class RecipientForm(FlaskForm):
    nickname = StringField('Tên/Biệt danh', validators=[DataRequired()])
    address = StringField('Địa chỉ (nhập để tìm hoặc chọn trên bản đồ)', validators=[Optional()])
    latitude = HiddenField('Vĩ độ', validators=[Optional()])
    longitude = HiddenField('Kinh độ', validators=[Optional()])
    has_kitchen = BooleanField('Có bếp nấu?')
    # Create choices from the RecipientType Enum
    recipient_type = SelectField(
        'Loại người nhận',
        choices=[(choice.value, choice.name.replace('_', ' ').title()) for choice in RecipientType],
        validators=[DataRequired()]
    )
    note = TextAreaField('Ghi chú đặc biệt (tùy chọn)', validators=[Optional()])
    submit = SubmitField('Thêm người nhận') 