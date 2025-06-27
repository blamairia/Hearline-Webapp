"""
Patient Repository for Heartline Desktop Application

This module provides data access methods for Patient entities.
"""

from typing import List, Optional
from sqlalchemy import and_, or_
from datetime import date

from .base import BaseRepository
from ..models.complete_models import Patient

class PatientRepository(BaseRepository[Patient]):
    """Repository for Patient entities"""
    
    def __init__(self):
        super().__init__(Patient)
    
    def search_patients(self, search_term: str, limit: int = 50) -> List[Patient]:
        """Search patients by name, phone, or email"""
        search_fields = ["first_name", "last_name", "phone", "email"]
        return self.search(search_fields, search_term, limit)
    
    def get_patients_by_age_range(self, min_age: int, max_age: int) -> List[Patient]:
        """Get patients within age range"""
        try:
            today = date.today()
            max_birth_date = date(today.year - min_age, today.month, today.day)
            min_birth_date = date(today.year - max_age, today.month, today.day)
            
            query = self.session.query(self.model).filter(
                and_(
                    self.model.date_of_birth >= min_birth_date,
                    self.model.date_of_birth <= max_birth_date
                )
            )
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting patients by age range: {str(e)}")
    
    def get_patients_by_gender(self, gender: str) -> List[Patient]:
        """Get patients by gender"""
        return self.get_many_by_field("gender", gender)
    
    def get_recent_patients(self, limit: int = 10) -> List[Patient]:
        """Get most recently added patients"""
        return self.get_all(limit=limit, order_by="created_at", desc_order=True)
    
    def get_patients_with_visits(self) -> List[Patient]:
        """Get patients who have at least one visit"""
        try:
            query = self.session.query(self.model).join(self.model.visits)
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting patients with visits: {str(e)}")
    
    def find_by_email(self, email: str) -> Optional[Patient]:
        """Find patient by email address"""
        return self.get_by_field("email", email)
    
    def find_by_phone(self, phone: str) -> Optional[Patient]:
        """Find patient by phone number"""
        return self.get_by_field("phone", phone)
