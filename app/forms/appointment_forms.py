# app/forms/appointment_forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeField, StringField
from wtforms.validators import DataRequired, Length, Optional
from datetime import datetime


def coerce_int_or_none(value):
    """Coerce to int, but return None for empty strings."""
    if value == '' or value is None:
        return None
    return int(value)


class AppointmentForm(FlaskForm):
    """Form for appointment creation and editing."""
    patient_id = SelectField("Patient", choices=[], coerce=int, validators=[DataRequired()])
    doctor_id = SelectField("Doctor", choices=[], coerce=coerce_int_or_none, validators=[Optional()])
    date = DateTimeField(
        "Appointment Date & Time",
        default=datetime.utcnow,
        format="%Y-%m-%d %H:%M",
        validators=[DataRequired()],
    )
    reason = StringField("Reason for Appointment", validators=[DataRequired(), Length(max=200)])
    state = SelectField(
        "Status",
        choices=[("scheduled", "Scheduled"), ("completed", "Completed"), ("canceled", "Canceled")],
        default="scheduled",
        validators=[DataRequired()],
    )
