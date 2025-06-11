# app/models/base.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize extensions (imported by extensions.py)
db = SQLAlchemy()
bcrypt = Bcrypt()
