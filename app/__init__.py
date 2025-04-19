from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure Jinja Do extension is enabled
    app.jinja_env.add_extension('jinja2.ext.do')

    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize Flask-Admin
    admin = Admin(app, name='SAVINA Admin', template_mode='bootstrap4')

    # Import models here for Admin registration
    from app.models import User, Recipient, Hub, Donation, Volunteer, VolunteerReport, DeliveryRoute, Delivery

    # Add administrative views here
    # TODO: Add authentication to these views!
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Recipient, db.session))
    admin.add_view(ModelView(Hub, db.session))
    admin.add_view(ModelView(Donation, db.session))
    # Add views for other models as needed
    # admin.add_view(ModelView(Volunteer, db.session))
    # admin.add_view(ModelView(VolunteerReport, db.session))
    # admin.add_view(ModelView(DeliveryRoute, db.session))
    # admin.add_view(ModelView(Delivery, db.session))

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.donations import bp as donations_bp
    app.register_blueprint(donations_bp, url_prefix='/donations')

    from app.info import bp as info_bp
    app.register_blueprint(info_bp)

    from app.volunteer import bp as volunteer_bp
    app.register_blueprint(volunteer_bp, url_prefix='/volunteer')

    # Register the supply admin blueprint
    from app.supply_admin import bp as supply_admin_bp
    app.register_blueprint(supply_admin_bp)

    # Register the new demand admin blueprint
    from app.demand_admin import bp as demand_admin_bp
    app.register_blueprint(demand_admin_bp)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

# Import models here to make them available for migrations
from app import models 