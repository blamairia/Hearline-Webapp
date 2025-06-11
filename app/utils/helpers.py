# app/utils/helpers.py

import os
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename, allowed_extensions):
    """Check if file has allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_upload_path(upload_type, filename):
    """Get the full path for uploaded file."""
    if upload_type == 'ecg':
        return os.path.join(current_app.config['ECG_UPLOAD_FOLDER'], filename)
    elif upload_type == 'docs':
        return os.path.join(current_app.config['DOCS_UPLOAD_FOLDER'], filename)
    else:
        return os.path.join(current_app.config['UPLOAD_FOLDER'], filename)


def save_uploaded_file(file, upload_type):
    """Save uploaded file and return the file path."""
    if file and file.filename:
        filename = secure_filename(file.filename)
        filepath = get_upload_path(upload_type, filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        file.save(filepath)
        return filepath
    return None
