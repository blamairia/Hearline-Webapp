"""
Appointment Widget - Placeholder
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AppointmentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Appointment Management - Under Development"))
    
    def new_appointment(self):
        """Create new appointment"""
        pass
