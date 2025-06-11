# app/models/user.py

from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt


class User(UserMixin, db.Model):
    """User model for authentication with role-based access control."""
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='assistant')  # 'doctor' or 'assistant'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Optional reference to doctor record (only for doctor users)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=True)
    
    # Additional profile information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationship to doctor (for doctor users)
    doctor = db.relationship("Doctor", backref="user", uselist=False)
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def has_role(self, role):
        """Check if user has specific role."""
        return self.role == role
    
    def is_doctor(self):
        """Check if user is a doctor."""
        return self.role == 'doctor'
    
    def is_assistant(self):
        """Check if user is an assistant."""
        return self.role == 'assistant'
    
    def get_full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.username}>'


class UserSession(db.Model):
    """Model to track user sessions for better security."""
    __tablename__ = "user_session"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 support
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    user = db.relationship("User", backref="sessions")
    
    def is_expired(self):
        """Check if session is expired."""
        return datetime.utcnow() > self.expires_at
    
    def __repr__(self):
        return f'<UserSession {self.session_token}>'
