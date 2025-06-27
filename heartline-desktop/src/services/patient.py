"""
Patient Service for Heartline Desktop Application

This service handles all patient-related business logic including
CRUD operations, search, and patient statistics.
"""

from typing import List, Optional, Dict
from datetime import datetime, date
import logging

from ..repositories.base import BaseRepository
from ..models.patient import Patient, Gender
from ..core.exceptions import ValidationError, BusinessLogicError

logger = logging.getLogger(__name__)

class PatientService:
    """Service for patient management"""
    
    def __init__(self):
        self.patient_repository = BaseRepository(Patient)
    
    def create_patient(self, patient_data: Dict) -> Patient:
        """Create a new patient with validation"""
        try:
            # Validate required fields
            self._validate_patient_data(patient_data)
            
            # Create patient
            patient = self.patient_repository.create(**patient_data)
            logger.info(f"Created new patient: {patient.full_name}")
            return patient
            
        except Exception as e:
            logger.error(f"Failed to create patient: {e}")
            raise BusinessLogicError(f"Patient creation failed: {e}")
    
    def get_patient(self, patient_id: int) -> Optional[Patient]:
        """Get patient by ID"""
        return self.patient_repository.get_by_id(patient_id)
    
    def get_all_patients(self) -> List[Patient]:
        """Get all active patients"""
        return self.patient_repository.get_all()
    
    def update_patient(self, patient_id: int, update_data: Dict) -> Optional[Patient]:
        """Update patient information"""
        try:
            # Validate update data
            self._validate_patient_data(update_data, is_update=True)
            
            # Update patient
            patient = self.patient_repository.update(patient_id, **update_data)
            if patient:
                logger.info(f"Updated patient: {patient.full_name}")
            return patient
            
        except Exception as e:
            logger.error(f"Failed to update patient: {e}")
            raise BusinessLogicError(f"Patient update failed: {e}")
    
    def delete_patient(self, patient_id: int) -> bool:
        """Soft delete patient"""
        try:
            success = self.patient_repository.delete(patient_id)
            if success:
                logger.info(f"Deleted patient ID: {patient_id}")
            return success
            
        except Exception as e:
            logger.error(f"Failed to delete patient: {e}")
            raise BusinessLogicError(f"Patient deletion failed: {e}")
    
    def search_patients(self, search_term: str) -> List[Patient]:
        """Search patients by name"""
        try:
            # This is a simplified search - in a real implementation,
            # you would use more sophisticated search logic
            all_patients = self.get_all_patients()
            
            search_term = search_term.lower()
            results = []
            
            for patient in all_patients:
                if (search_term in patient.first_name.lower() or 
                    search_term in patient.last_name.lower() or
                    search_term in patient.full_name.lower()):
                    results.append(patient)
            
            return results
            
        except Exception as e:
            logger.error(f"Patient search failed: {e}")
            raise BusinessLogicError(f"Search failed: {e}")
    
    def get_patient_statistics(self) -> Dict:
        """Get patient statistics"""
        try:
            all_patients = self.get_all_patients()
            
            stats = {
                "total_patients": len(all_patients),
                "male_patients": len([p for p in all_patients if p.gender == Gender.MALE]),
                "female_patients": len([p for p in all_patients if p.gender == Gender.FEMALE]),
                "age_groups": self._calculate_age_groups(all_patients),
                "recent_registrations": self._count_recent_registrations(all_patients)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get patient statistics: {e}")
            raise BusinessLogicError(f"Statistics calculation failed: {e}")
    
    def _validate_patient_data(self, data: Dict, is_update: bool = False):
        """Validate patient data"""
        required_fields = ['first_name', 'last_name', 'date_of_birth', 'gender']
        
        if not is_update:
            for field in required_fields:
                if field not in data or not data[field]:
                    raise ValidationError(f"Required field missing: {field}")
        
        # Validate gender
        if 'gender' in data:
            if isinstance(data['gender'], str):
                try:
                    data['gender'] = Gender(data['gender'].lower())
                except ValueError:
                    raise ValidationError("Invalid gender value")
        
        # Validate date of birth
        if 'date_of_birth' in data:
            if isinstance(data['date_of_birth'], str):
                try:
                    data['date_of_birth'] = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                except ValueError:
                    raise ValidationError("Invalid date format. Use YYYY-MM-DD")
            
            # Check if date is not in the future
            if data['date_of_birth'] > date.today():
                raise ValidationError("Date of birth cannot be in the future")
        
        # Validate email format (basic)
        if 'email' in data and data['email']:
            if '@' not in data['email'] or '.' not in data['email']:
                raise ValidationError("Invalid email format")
    
    def _calculate_age_groups(self, patients: List[Patient]) -> Dict:
        """Calculate age group distribution"""
        age_groups = {
            "0-18": 0,
            "19-35": 0,
            "36-55": 0,
            "56-75": 0,
            "75+": 0
        }
        
        for patient in patients:
            age = patient.age
            if age <= 18:
                age_groups["0-18"] += 1
            elif age <= 35:
                age_groups["19-35"] += 1
            elif age <= 55:
                age_groups["36-55"] += 1
            elif age <= 75:
                age_groups["56-75"] += 1
            else:
                age_groups["75+"] += 1
        
        return age_groups
    
    def _count_recent_registrations(self, patients: List[Patient]) -> int:
        """Count patients registered in the last 30 days"""
        from datetime import timedelta
        
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        return len([p for p in patients if p.created_at >= thirty_days_ago])
