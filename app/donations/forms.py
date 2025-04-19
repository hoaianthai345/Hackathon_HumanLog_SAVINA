# Donations forms go here 
from flask_wtf import FlaskForm
from wtforms import StringField, TelField, EmailField, TextAreaField, SelectField, SelectMultipleField, BooleanField, DateField, FloatField, FieldList, FormField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional, Email, Length, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput # For SelectMultipleField with checkboxes
from app.models import Hub # To query hubs for dropdown

# Define common choices
FOOD_CATEGORIES = [
    ('', '-- Chọn loại --'),
    ('rau_cu', 'Rau củ'),
    ('trai_cay', 'Trái cây'),
    ('thit_ca', 'Thịt/Cá tươi'),
    ('trung_sua', 'Trứng/Sữa'),
    ('com_chin', 'Cơm/Đồ ăn chín'),
    ('do_kho', 'Đồ khô (gạo, mì, ...)'),
    ('gia_vi', 'Gia vị'),
    ('banh_keo', 'Bánh kẹo'),
    ('do_hop', 'Đồ hộp'),
    ('nuoc_uong', 'Nước uống'),
    ('khac', 'Khác')
]

UNIT_CHOICES = [
    ('', '-- Chọn đơn vị --'),
    ('kg', 'kg'),
    ('gam', 'gam'),
    ('cai', 'Cái/Trái/Củ'),
    ('bo', 'Bó'),
    ('hop', 'Hộp'),
    ('chai', 'Chai'),
    ('lon', 'Lon'),
    ('goi', 'Gói'),
    ('thung', 'Thùng'),
    ('phan_an', 'Phần ăn'),
    ('suat_com', 'Suất cơm'),
    ('lit', 'Lít'),
    ('ml', 'ml'),
    ('khac', 'Khác')
]

AVAILABILITY_CHOICES = [
    ('sang', 'Sáng (8h-11h)'),
    ('trua', 'Trưa (11h-13h)'),
    ('chieu', 'Chiều (13h-17h)'),
    ('toi', 'Tối (sau 17h)')
]

# --- Sub-form for individual food items ---
class FoodItemForm(FlaskForm):
    # Need a dummy class for WTForms FieldList, actual fields are inside
    category = SelectField('Loại thực phẩm', choices=FOOD_CATEGORIES, validators=[DataRequired(message='Vui lòng chọn loại thực phẩm.')])
    quantity = FloatField('Số lượng', validators=[DataRequired(message='Vui lòng nhập số lượng.')])
    unit = SelectField('Đơn vị', choices=UNIT_CHOICES, validators=[DataRequired(message='Vui lòng chọn đơn vị.')])
    # DateField requires format specification if not default
    expiry_date = DateField('Hạn sử dụng (Nếu đồ chín, chọn trong ngày)', format='%Y-%m-%d', validators=[Optional()])
    notes = TextAreaField('Ghi chú cho món này', validators=[Optional()])

# --- Main Donation Form ---
class DonationForm(FlaskForm):
    # Donor Info
    donor_name = StringField('Tên đơn vị / Cá nhân', validators=[DataRequired()])
    contact_person = StringField('Người liên hệ', validators=[DataRequired()])
    phone = TelField('Số điện thoại', validators=[DataRequired(), Length(min=10, max=15)])
    email = EmailField('Email', validators=[Optional(), Email()])
    pickup_address = TextAreaField('Địa chỉ lấy hàng', validators=[DataRequired()])

    # Food Items (Dynamic List)
    food_items = FieldList(FormField(FoodItemForm), min_entries=1, label='Thông tin thực phẩm')

    # Logistics
    # Using SelectMultipleField with CheckboxInput for multiple selections
    availability_window = SelectMultipleField(
        'Thời gian có thể giao/nhận',
        choices=AVAILABILITY_CHOICES,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
        validators=[DataRequired(message='Vui lòng chọn ít nhất một khung giờ.')]
    )
    requires_pickup = BooleanField('Cần người đến lấy hàng?', default=True)

    # Dropoff Hub (Optional, only if requires_pickup is False)
    # Use HiddenField initially, logic to show/hide and validate based on requires_pickup will be in JS/template
    # We can add QuerySelectField later if needed directly in the form
    intended_dropoff_hub_id = HiddenField('Hub muốn giao đến (nếu tự giao)', validators=[Optional()])
    # TODO: Add a non-hidden SelectField in the template, populate it with Hubs via JS/context,
    #       and update the hidden field value based on selection.

    submit = SubmitField('Xác nhận đóng góp')

    # Custom validation example: ensure dropoff hub is selected if requires_pickup is false
    # def validate_intended_dropoff_hub_id(self, field):
    #     if not self.requires_pickup.data and not field.data:
    #         raise ValidationError('Vui lòng chọn Hub bạn sẽ giao hàng đến.') 