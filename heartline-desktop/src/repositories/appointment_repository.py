"""
Appointment Repository for Heartline Desktop Application

This module provides data access methods for Appointment entities.
"""

from typing import List, Optional
from datetime import datetime, date, timedelta
from sqlalchemy import and_, func

from .base import BaseRepository
from ..models.complete_models import Appointment

class AppointmentRepository(BaseRepository[Appointment]):
    """Repository for Appointment entities"""
    
    def __init__(self):
        super().__init__(Appointment)
    
    def get_appointments_by_date(self, target_date: date) -> List[Appointment]:
        """Get all appointments for a specific date"""
        try:
            start_datetime = datetime.combine(target_date, datetime.min.time())
            end_datetime = datetime.combine(target_date, datetime.max.time())
            
            query = self.session.query(self.model).filter(
                and_(
                    self.model.date >= start_datetime,
                    self.model.date <= end_datetime
                )
            ).order_by(self.model.date)
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting appointments by date: {str(e)}")
    
    def get_appointments_by_date_range(self, start_date: date, end_date: date) -> List[Appointment]:
        """Get appointments within a date range"""
        try:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
            
            query = self.session.query(self.model).filter(
                and_(
                    self.model.date >= start_datetime,
                    self.model.date <= end_datetime
                )
            ).order_by(self.model.date)
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting appointments by date range: {str(e)}")
    
    def get_appointments_by_patient(self, patient_id: int) -> List[Appointment]:
        """Get all appointments for a specific patient"""
        return self.get_many_by_field("patient_id", patient_id)
    
    def get_appointments_by_doctor(self, doctor_id: int) -> List[Appointment]:
        """Get all appointments for a specific doctor"""
        return self.get_many_by_field("doctor_id", doctor_id)
    
    def get_appointments_by_state(self, state: str) -> List[Appointment]:
        """Get appointments by state (scheduled, completed, canceled)"""
        return self.get_many_by_field("state", state)
    
    def get_today_appointments(self) -> List[Appointment]:
        """Get all appointments for today"""
        return self.get_appointments_by_date(date.today())
    
    def get_upcoming_appointments(self, days: int = 7) -> List[Appointment]:
        """Get upcoming appointments within specified days"""
        start_date = date.today()
        end_date = start_date + timedelta(days=days)
        return self.get_appointments_by_date_range(start_date, end_date)
    
    def get_overdue_appointments(self) -> List[Appointment]:
        """Get appointments that are overdue (past date but still scheduled)"""
        try:
            now = datetime.now()
            query = self.session.query(self.model).filter(
                and_(
                    self.model.date < now,
                    self.model.state == "scheduled"
                )
            ).order_by(self.model.date)
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting overdue appointments: {str(e)}")
    
    def count_appointments_by_date(self, target_date: date) -> int:
        """Count appointments for a specific date"""
        try:
            start_datetime = datetime.combine(target_date, datetime.min.time())
            end_datetime = datetime.combine(target_date, datetime.max.time())
            
            count = self.session.query(self.model).filter(
                and_(
                    self.model.date >= start_datetime,
                    self.model.date <= end_datetime
                )
            ).count()
            
            return count
        except Exception as e:
            raise Exception(f"Error counting appointments by date: {str(e)}")
    
    def get_appointment_conflicts(self, doctor_id: int, appointment_date: datetime, 
                                 duration_minutes: int = 30, exclude_id: Optional[int] = None) -> List[Appointment]:
        """Check for appointment conflicts for a doctor"""
        try:
            start_time = appointment_date
            end_time = appointment_date + timedelta(minutes=duration_minutes)
            
            query = self.session.query(self.model).filter(
                and_(
                    self.model.doctor_id == doctor_id,
                    self.model.state == "scheduled",
                    self.model.date < end_time,
                    self.model.date >= start_time - timedelta(minutes=duration_minutes)
                )
            )
            
            if exclude_id:
                query = query.filter(self.model.id != exclude_id)
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error checking appointment conflicts: {str(e)}")
