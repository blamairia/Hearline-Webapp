"""
Heartline Desktop Application

A comprehensive doctor cabinet management system built with PyQt6 and Material Design.
Provides native desktop experience with the same core functionalities as the web application.

Features:
- Patient Management with advanced search and filtering
- AI-powered ECG Analysis using ONNX Runtime
- Appointment Scheduling with calendar view
- Prescription Management with 7000+ Algerian medications
- Visit Documentation and Medical Records
- Real-time Waiting List Management
- Multi-user support with role-based access control

Author: Heartline Development Team
Version: 1.0.0
"""

import sys
import os
from pathlib import Path

# Clear any cached database environment variables FIRST
db_vars_to_clear = [
    'DATABASE_URL', 'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME'
]
for var in db_vars_to_clear:
    if var in os.environ:
        del os.environ[var]

# Force load .env file before any other imports
from dotenv import load_dotenv
load_dotenv(override=True)

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QIcon, QFont, QPalette
import qt_material

from src.core.config import Config, config
from src.core.database import db_manager
from src.ui.main_window import MainWindow
from src.utils.logger import setup_logging

def setup_application():
    """Setup application configuration and styling"""
    
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    # Note: AA_EnableHighDpiScaling is deprecated in Qt 6.x
    # High DPI scaling is enabled by default
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    app.setOrganizationName("Heartline Medical")
    app.setOrganizationDomain("heartline.medical")
    
    # Set application icon
    icon_path = Path(__file__).parent / "assets" / "icons" / "heartline.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Apply Material Design theme
    try:
        qt_material.apply_stylesheet(app, theme=config.THEME)
        
        # Customize the theme with medical colors
        app.setStyleSheet(app.styleSheet() + """
            QMainWindow {
                background-color: #f5f5f5;
            }
            .patient-card {
                background-color: white;
                border-radius: 8px;
                padding: 16px;
                margin: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .primary-button {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            .primary-button:hover {
                background-color: #1976D2;
            }
            .danger-button {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            .danger-button:hover {
                background-color: #D32F2F;
            }
            .success-button {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            .success-button:hover {
                background-color: #388E3C;
            }
        """)
    except Exception as e:
        print(f"Warning: Could not apply Material Design theme: {e}")
    
    return app

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import qt_material
        import onnxruntime
        import psycopg2
        import sqlalchemy
        return True
    except ImportError as e:
        QMessageBox.critical(
            None,
            "Missing Dependencies",
            f"Required dependency not found: {e}\n\n"
            "Please install all dependencies using:\n"
            "pip install -r requirements.txt"
        )
        return False

def main():
    """Main entry point for Heartline Desktop Application"""
    
    # Setup logging
    setup_logging()
    
    # Ensure required directories exist
    Config.ensure_directories()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup application
    app = setup_application()
    
    # Initialize database
    if not db_manager.initialize():
        QMessageBox.critical(
            None,
            "Database Error",
            "Failed to connect to the database.\n\n"
            "Please check your database configuration in the .env file."
        )
        sys.exit(1)
    
    try:
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Start application event loop
        sys.exit(app.exec())
        
    except Exception as e:
        QMessageBox.critical(
            None,
            "Application Error",
            f"An unexpected error occurred:\n{str(e)}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
