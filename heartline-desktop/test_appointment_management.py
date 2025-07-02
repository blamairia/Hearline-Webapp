"""
Test script for Appointment Management System

This script tests the appointment management functionality including:
- Appointment dialog creation and editing
- Enhanced appointment table with all fields
- CRUD operations
- Patient and doctor selection
"""

import sys
import os
from datetime import datetime, timedelta

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from src.core.database import db_manager
from src.ui.components.tables.appointments_table import AppointmentsTableWidget
from src.ui.appointment_management.dialogs.appointment_dialog import AppointmentDialog
from src.models.complete_models import Appointment, Patient, Doctor


class TestAppointmentManagement(QMainWindow):
    """Test window for appointment management"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Appointment Management Test")
        self.setGeometry(100, 100, 1400, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Add appointment table widget
        self.appointment_table = AppointmentsTableWidget()
        layout.addWidget(self.appointment_table)
        
        # Initialize database and create sample data
        self.initialize_test_data()
    
    def initialize_test_data(self):
        """Initialize database and create sample appointment data if needed"""
        try:
            # Initialize database
            db_manager.initialize()
            
            with db_manager.get_session() as session:
                # Check if we have any appointments
                appointment_count = session.query(Appointment).count()
                
                if appointment_count == 0:
                    print("Creating sample appointment data...")
                    
                    # Get existing patients and doctors
                    patients = session.query(Patient).limit(3).all()
                    doctors = session.query(Doctor).limit(2).all()
                    
                    if patients and doctors:
                        # Create sample appointments
                        sample_appointments = [
                            {
                                'patient_id': patients[0].id,
                                'doctor_id': doctors[0].id,
                                'date': datetime.now() + timedelta(days=1, hours=9),
                                'reason': 'Regular checkup and blood pressure monitoring',
                                'appointment_type': 'consultation',
                                'duration_minutes': 30,
                                'priority': 'normal',
                                'state': 'scheduled',
                                'confirmed': False,
                                'reminder_sent': False,
                                'notes': 'Patient prefers morning appointments'
                            },
                            {
                                'patient_id': patients[1].id,
                                'doctor_id': doctors[0].id,
                                'date': datetime.now() + timedelta(days=2, hours=14),
                                'reason': 'Follow-up visit for cardiac evaluation',
                                'appointment_type': 'follow_up',
                                'duration_minutes': 45,
                                'priority': 'high',
                                'state': 'confirmed',
                                'confirmed': True,
                                'reminder_sent': True,
                                'notes': 'Review ECG results and adjust medication'
                            },
                            {
                                'patient_id': patients[2].id,
                                'doctor_id': doctors[1].id if len(doctors) > 1 else doctors[0].id,
                                'date': datetime.now() + timedelta(days=3, hours=10, minutes=30),
                                'reason': 'Emergency consultation for chest pain',
                                'appointment_type': 'emergency',
                                'duration_minutes': 60,
                                'priority': 'urgent',
                                'state': 'scheduled',
                                'confirmed': False,
                                'reminder_sent': False,
                                'notes': 'Patient reports intermittent chest pain',
                                'patient_notes': 'Please bring recent lab results'
                            },
                            {
                                'patient_id': patients[0].id,
                                'doctor_id': None,  # No doctor assigned
                                'date': datetime.now() + timedelta(days=7, hours=11),
                                'reason': 'Annual physical examination',
                                'appointment_type': 'check_up',
                                'duration_minutes': 30,
                                'priority': 'low',
                                'state': 'pending',
                                'confirmed': False,
                                'reminder_sent': False,
                                'notes': 'Schedule with available doctor'
                            },
                            {
                                'patient_id': patients[1].id,
                                'doctor_id': doctors[0].id,
                                'date': datetime.now() - timedelta(days=1, hours=10),  # Past appointment
                                'reason': 'Post-surgery follow-up',
                                'appointment_type': 'follow_up',
                                'duration_minutes': 30,
                                'priority': 'normal',
                                'state': 'completed',
                                'confirmed': True,
                                'reminder_sent': True,
                                'notes': 'Surgery recovery progressing well'
                            }
                        ]
                        
                        for apt_data in sample_appointments:
                            appointment = Appointment(**apt_data)
                            appointment.created_at = datetime.now()
                            appointment.updated_at = datetime.now()
                            session.add(appointment)
                        
                        session.commit()
                        print(f"Created {len(sample_appointments)} sample appointments")
                    else:
                        print("No patients or doctors found. Please create patients and doctors first.")
                else:
                    print(f"Found {appointment_count} existing appointments")
            
        except Exception as e:
            print(f"Error initializing test data: {e}")


def main():
    """Main function to run the appointment management test"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Heartline Appointment Management Test")
    app.setApplicationVersion("1.0")
    
    # Create and show the test window
    window = TestAppointmentManagement()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
