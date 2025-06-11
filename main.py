# main.py

from app import create_app
from app.services.ecg_service import ECGService

app = create_app()

if __name__ == "__main__":
    # Initialize ECG service on startup
    with app.app_context():
        ecg_service = ECGService()
    
    app.run(host='0.0.0.0', debug=False)
