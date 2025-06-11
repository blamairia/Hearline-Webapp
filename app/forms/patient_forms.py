# app/forms/patient_forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Optional, Email


class PatientForm(FlaskForm):
    """Form for creating and editing patients."""
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=50)])
    date_of_birth = DateField("Date of Birth", format="%Y-%m-%d", validators=[DataRequired()])
    gender = SelectField(
        "Gender",
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        validators=[DataRequired()],
    )
    address = TextAreaField("Address", validators=[Optional()])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    email = StringField("Email", validators=[Optional(), Email()])
    medical_history = TextAreaField("Medical History", validators=[Optional()])
