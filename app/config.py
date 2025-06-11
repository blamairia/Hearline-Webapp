# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for Flask application."""
    
    # Basic Flask configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "replace-this-with-a-secure-random-string")
    
    # Database configuration
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT") 
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    
    if not all([DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME]):
        raise ValueError("Missing required database environment variables. Please check your .env file.")
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload configuration
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ECG_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "ecg_files")
    DOCS_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "visit_docs")
    
    # ECG Model configuration
    ECG_MODEL_PATH = os.path.join(BASE_DIR, "resnet34_model.pth")
    
    # Ensure upload directories exist
    os.makedirs(ECG_UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(DOCS_UPLOAD_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
