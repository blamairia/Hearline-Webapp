import unittest
import sys
import os

# Add the application directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, User

class TestUIElements(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            # Create a test user
            user = User(username='testadmin', email='test@example.com', role='doctor')
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_login_page_structure(self):
        """Test that the new login page loads with the correct structure."""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        
        # Check for the new auth layout elements
        self.assertIn('auth-card', html)
        self.assertIn('Heartline Medical', html)
        self.assertIn('Secure Clinical Access', html)
        # Check that the old blobs are gone
        self.assertNotIn('bg-blob', html)

    def test_dashboard_macros(self):
        """Test that the dashboard uses the new stat_card macro."""
        self.login('testadmin', 'testpass')
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        
        # Check for the macro output classes
        self.assertIn('stat-card', html)
        self.assertIn('stat-icon text-primary bg-primary-subtle', html)
        
        # Check for the new Quick Actions structure
        self.assertIn('Start New Visit', html)
        self.assertIn('Check-in & Vitals', html)

    def test_patients_table_buttons(self):
        """Test that the patients table has the standardized primary button."""
        self.login('testadmin', 'testpass')
        response = self.app.get('/patients_table')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        
        # Check for the standardized button class
        self.assertIn('btn btn-primary shadow-sm', html)
        self.assertIn('New Patient', html)
        
        # Check for macro usage
        self.assertIn('stat-icon text-success bg-success-subtle', html)

    def test_visits_table_buttons(self):
        """Test that the visits table has the standardized primary button."""
        self.login('testadmin', 'testpass')
        response = self.app.get('/visits_table')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        
        # Check for the standardized button class
        self.assertIn('btn btn-primary shadow-sm', html)
        self.assertIn('New Visit', html)

    def test_patient_details_structure(self):
        """Test that the patient details page uses the new classes."""
        self.login('testadmin', 'testpass')
        
        # Create a patient first
        from app import Patient
        from datetime import date
        with app.app_context():
            p = Patient(
                first_name='John',
                last_name='Doe',
                date_of_birth=date(1980, 1, 1),
                gender='Male',
                medical_history='Hypertension'
            )
            db.session.add(p)
            db.session.commit()
            p_id = p.id

        response = self.app.get(f'/patient/{p_id}')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        
        # Check for new classes
        self.assertIn('avatar-xl', html)
        self.assertIn('clinical-note', html)
        # Check content
        self.assertIn('John Doe', html)
        self.assertIn('Hypertension', html)

if __name__ == '__main__':
    unittest.main()