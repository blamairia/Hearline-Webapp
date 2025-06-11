# app/forms/visit_forms.py

from flask_wtf import FlaskForm
from wtforms import (
    Form, StringField, TextAreaField, SelectField, IntegerField,
    DecimalField, DateTimeField, FieldList, FormField, FileField
)
from wtforms.validators import DataRequired, Optional, NumberRange
from datetime import datetime


class PrescriptionForm(Form):
    """Subform for prescriptions."""
    medicament_num_enr = SelectField(
        "Medicament (num_enr)",
        choices=[],  # will populate in view
        validators=[DataRequired()],
    )
    dosage_instructions = TextAreaField("Dosage / Instructions", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])


class VisitDocumentForm(Form):
    """Subform for visit documents (blood/MRI/X-Ray)."""
    doc_type = SelectField(
        "Document Type",
        choices=[("blood", "Blood Work"), ("mri", "MRI Scan"), ("xray", "X-Ray Scan")],
        validators=[DataRequired()],
    )
    file_path = FileField("Upload File (PDF / Image)", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])


class VisitForm(FlaskForm):
    """Form for visit creation and editing with nested prescriptions and documents."""
    patient_id = IntegerField("Patient", validators=[DataRequired()])
    visit_date = DateTimeField(
        "Visit Date & Time",
        default=datetime.utcnow,
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()],
    )
    diagnosis = TextAreaField("Diagnosis", validators=[Optional()])
    follow_up_date = DateTimeField(
        "Follow-up Date & Time",
        format="%Y-%m-%dT%H:%M",
        validators=[Optional()],
    )
    ecg_mat = FileField("Upload .mat File", validators=[Optional()])
    ecg_hea = FileField("Upload .hea File", validators=[Optional()])

    payment_total = DecimalField("Payment Total", places=2, default=0.00, validators=[NumberRange(min=0)])
    payment_status = SelectField(
        "Payment Status",
        choices=[("paid", "Paid"), ("partial", "Partial"), ("unpaid", "Unpaid")],
        default="unpaid",
        validators=[DataRequired()],
    )
    payment_remaining = DecimalField("Payment Remaining", places=2, default=0.00, validators=[NumberRange(min=0)])

    # Allow up to 5 prescriptions per visit
    prescriptions = FieldList(FormField(PrescriptionForm), min_entries=1, max_entries=5)

    # Allow up to 3 scanned documents per visit
    documents = FieldList(FormField(VisitDocumentForm), min_entries=1, max_entries=3)
