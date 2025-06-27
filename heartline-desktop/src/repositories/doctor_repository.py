"""
Doctor Repository for Heartline Desktop Application

This module provides data access methods for Doctor entities.
"""

from typing import List, Optional

from .base import BaseRepository
from ..models.complete_models import Doctor

class DoctorRepository(BaseRepository[Doctor]):
    """Repository for Doctor entities"""
    
    def __init__(self):
        super().__init__(Doctor)
    
    def search_doctors(self, search_term: str, limit: int = 50) -> List[Doctor]:
        """Search doctors by name, specialty, or email"""
        search_fields = ["first_name", "last_name", "specialty", "email"]
        return self.search(search_fields, search_term, limit)
    
    def get_doctors_by_specialty(self, specialty: str) -> List[Doctor]:
        """Get doctors by specialty"""
        return self.get_many_by_field("specialty", specialty)
    
    def get_available_doctors(self) -> List[Doctor]:
        """Get all doctors (for now, all doctors are considered available)"""
        return self.get_all(order_by="last_name")
    
    def get_doctor_specialties(self) -> List[str]:
        """Get list of all unique specialties"""
        try:
            result = self.session.query(self.model.specialty).distinct().all()
            return [row[0] for row in result if row[0]]
        except Exception as e:
            raise Exception(f"Error getting doctor specialties: {str(e)}")
    
    def find_by_email(self, email: str) -> Optional[Doctor]:
        """Find doctor by email address"""
        return self.get_by_field("email", email)
    
    def get_doctors_with_appointments(self) -> List[Doctor]:
        """Get doctors who have appointments"""
        try:
            query = self.session.query(self.model).join(self.model.appointments)
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting doctors with appointments: {str(e)}")
