#!/usr/bin/env python3
"""
Test script for Doctor Management System

This script provides a standalone test of the doctor management functionality.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up environment
os.environ.setdefault('HEARTLINE_ENV', 'development')

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from src.ui.doctor_management import DoctorManagementWidget
from src.core.database import db_manager


class TestWindow(QMainWindow):
    """Test window for doctor management system"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the test window UI"""
        self.setWindowTitle("Doctor Management System - Test")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create doctor management widget
        self.doctor_widget = DoctorManagementWidget()
        layout.addWidget(self.doctor_widget)
    
    def closeEvent(self, event):
        """Handle close event"""
        db_manager.close()
        event.accept()


def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Heartline Doctor Management Test")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Heartline Medical")
    
    # Create and show main window
    window = TestWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
