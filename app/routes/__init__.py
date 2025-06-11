# app/routes/__init__.py

from .main import main_bp
from .auth import auth_bp
from .dashboard import dashboard_bp
from .patients import patients_bp
from .visits import visits_bp
from .appointments import appointments_bp
from .ecg import ecg_bp
from .api import api_bp

__all__ = ['main_bp', 'auth_bp', 'dashboard_bp', 'patients_bp', 'visits_bp', 'appointments_bp', 'ecg_bp', 'api_bp']
