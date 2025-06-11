# app/decorators/__init__.py

from .auth import role_required, doctor_required, assistant_required, any_role_required

__all__ = ['role_required', 'doctor_required', 'assistant_required', 'any_role_required']
