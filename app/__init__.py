# app/__init__.py

import os
from flask import Flask
from dotenv import load_dotenv

from app.extensions import db, bcrypt, login_manager, moment
from app.config import Config
from app.models import User
from app.utils.filters import register_template_filters

# Load environment variables
load_dotenv()


def create_app(config_class=Config):
    """Application factory pattern for creating Flask app instances."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register template filters
    register_template_filters(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.patients import patients_bp
    from app.routes.visits import visits_bp
    from app.routes.appointments import appointments_bp
    from app.routes.ecg import ecg_bp
    from app.routes.api import api_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(patients_bp, url_prefix='/patients')
    app.register_blueprint(visits_bp, url_prefix='/visits')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(ecg_bp, url_prefix='/ecg')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created/verified successfully.")
        except Exception as e:
            print(f"Database error: {e}")

    return app
