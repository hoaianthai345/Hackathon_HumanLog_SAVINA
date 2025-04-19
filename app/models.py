from app import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import enum

# Example User model - Can represent donors, admins, potentially link to Volunteers
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), index=True) # e.g., 'donor', 'volunteer', 'admin'
    # Relationship to Donations if User is a donor
    donations = db.relationship('Donation', foreign_keys='Donation.donor_user_id', backref='donor_user', lazy='dynamic')
    # Relationship if User is linked to a Volunteer profile
    volunteer_profile = db.relationship('Volunteer', backref='user_account', uselist=False) # One-to-one

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

# --- New Models Based on Schema ---

class HubType(enum.Enum):
    MAIN = 'main'
    MICRO = 'micro'
    DROP_OFF = 'drop-off'
    MOBILE = 'mobile'

class Hub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)
    hub_type = db.Column(db.Enum(HubType), default=HubType.MICRO, nullable=False)
    # Specify the foreign key using a string reference
    donations = db.relationship('Donation', foreign_keys='Donation.hub_id', backref='hub', lazy='dynamic')
    routes_originating = db.relationship('DeliveryRoute', backref='origin_hub', lazy='dynamic')
    # Optional: Define relationship for intended dropoffs if needed
    # intended_donations = db.relationship('Donation', foreign_keys='Donation.intended_dropoff_hub_id', backref='intended_dropoff_hub', lazy='dynamic')

    def __repr__(self):
        return f'<Hub {self.name} ({self.hub_type.value})>'

class DonationStatus(enum.Enum):
    PENDING_CONFIRMATION = 'pending_confirmation'
    AVAILABLE = 'available'
    ASSIGNED = 'assigned'
    DELIVERED = 'delivered'

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=True)
    donor_name = db.Column(db.String(150), nullable=True)
    contact_person = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    pickup_address = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100))
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(50))
    expiry_date = db.Column(db.DateTime, index=True, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    availability_window = db.Column(db.String(100), nullable=True)
    requires_pickup = db.Column(db.Boolean, default=True, nullable=False)
    intended_dropoff_hub_id = db.Column(db.Integer, db.ForeignKey('hub.id'), nullable=True)
    hub_id = db.Column(db.Integer, db.ForeignKey('hub.id'), nullable=True)
    status = db.Column(db.Enum(DonationStatus), default=DonationStatus.PENDING_CONFIRMATION, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    delivery = db.relationship('Delivery', backref='donation_item', lazy='dynamic')

    def __repr__(self):
        donor = self.donor_user.username if self.donor_user else self.donor_name
        return f'<Donation {self.id} by {donor} - {self.status.value}>'

class RecipientType(enum.Enum):
    HOUSEHOLD = 'household'
    HOMELESS = 'homeless'
    TEMPORARY = 'temporary'

class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), index=True)
    address = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)
    has_kitchen = db.Column(db.Boolean, default=False)
    recipient_type = db.Column(db.Enum(RecipientType), default=RecipientType.HOMELESS, nullable=False)
    note = db.Column(db.Text)
    reports = db.relationship('VolunteerReport', backref='recipient', lazy='dynamic')
    deliveries = db.relationship('Delivery', backref='recipient', lazy='dynamic')

    def __repr__(self):
        return f'<Recipient {self.nickname or self.id}>'

class VolunteerRole(enum.Enum):
    DRIVER = 'driver'
    REPORTER = 'reporter'
    COORDINATOR = 'coordinator'

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=True) # Link to User account
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True)
    area = db.Column(db.Text) # Operating area description
    rating = db.Column(db.Float, default=5.0)
    volunteer_role = db.Column(db.Enum(VolunteerRole), nullable=False, index=True)
    reports_filed = db.relationship('VolunteerReport', backref='volunteer', lazy='dynamic')
    routes_assigned = db.relationship('DeliveryRoute', backref='volunteer', lazy='dynamic')

    def __repr__(self):
        return f'<Volunteer {self.name} ({self.volunteer_role.value})>'

class VolunteerReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    image_url = db.Column(db.String(255))
    notes = db.Column(db.Text) # Added notes field based on description

    def __repr__(self):
        return f'<Report {self.id} by Vol:{self.volunteer_id} for Rec:{self.recipient_id}>'

class RouteStatus(enum.Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    CANCELLED = 'cancelled' # Added cancelled status

class DeliveryRoute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'), index=True, nullable=True) # Can be initially unassigned
    hub_id = db.Column(db.Integer, db.ForeignKey('hub.id'), nullable=False)
    status = db.Column(db.Enum(RouteStatus), default=RouteStatus.PENDING, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # Relationship to individual deliveries within this route
    deliveries = db.relationship('Delivery', backref='route', lazy='dynamic')

    def __repr__(self):
        return f'<Route {self.id} from Hub:{self.hub_id} - {self.status.value}>'

class DeliveryStatus(enum.Enum):
    ASSIGNED = 'assigned'
    DELIVERED = 'delivered'
    FAILED = 'failed'

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('delivery_route.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'), nullable=False)
    donation_id = db.Column(db.Integer, db.ForeignKey('donation.id'), nullable=False, unique=True) # Assuming one donation item per delivery task for simplicity
    status = db.Column(db.Enum(DeliveryStatus), default=DeliveryStatus.ASSIGNED, nullable=False, index=True)
    confirmation_image = db.Column(db.String(255))
    notes = db.Column(db.Text) # Added notes field
    delivered_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Delivery {self.id} for Rec:{self.recipient_id} - {self.status.value}>' 