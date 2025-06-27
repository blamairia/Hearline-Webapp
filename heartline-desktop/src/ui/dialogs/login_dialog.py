"""
Login Dialog - Placeholder
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Login Dialog - Under Development"))
        
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.accept)
        layout.addWidget(login_btn)
        
        self.user = None
    
    def get_user(self):
        """Return mock user for now"""
        class MockUser:
            def __init__(self):
                self.username = "admin"
                self.full_name = "Administrator"
                self.role = "doctor"
        
        return MockUser()
