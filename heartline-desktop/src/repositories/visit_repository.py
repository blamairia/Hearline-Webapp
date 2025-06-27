"""
Visit Repository for Heartline Desktop Application

This module provides data access methods for Visit entities.
"""

from typing import List, Optional
from datetime import datetime, date, timedelta
from sqlalchemy import and_, func

from .base import BaseRepository
from ..models.complete_models import Visit

class VisitRepository(BaseRepository[Visit]):
    """Repository for Visit entities"""
    
    def __init__(self):
        super().__init__(Visit)
    
    def get_visits_by_patient(self, patient_id: int) -> List[Visit]:
        """Get all visits for a specific patient"""
        return self.get_many_by_field("patient_id", patient_id)
    
    def get_visits_by_doctor(self, doctor_id: int) -> List[Visit]:
        """Get all visits for a specific doctor"""
        return self.get_many_by_field("doctor_id", doctor_id)
    
    def get_visits_by_date(self, target_date: date) -> List[Visit]:
        """Get all visits for a specific date"""
        try:
            start_datetime = datetime.combine(target_date, datetime.min.time())
            end_datetime = datetime.combine(target_date, datetime.max.time())
            
            query = self.session.query(self.model).filter(
                and_(
                    self.model.visit_date >= start_datetime,
                    self.model.visit_date <= end_datetime
                )
            ).order_by(self.model.visit_date)
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting visits by date: {str(e)}")
    
    def get_visits_by_date_range(self, start_date: date, end_date: date) -> List[Visit]:
        """Get visits within a date range"""
        try:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
            
            query = self.session.query(self.model).filter(
                and_(
                    self.model.visit_date >= start_datetime,
                    self.model.visit_date <= end_datetime
                )
            ).order_by(self.model.visit_date)
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting visits by date range: {str(e)}")
    
    def get_recent_visits(self, limit: int = 20) -> List[Visit]:
        """Get most recent visits"""
        return self.get_all(limit=limit, order_by="visit_date", desc_order=True)
    
    def get_visits_with_ecg(self) -> List[Visit]:
        """Get visits that have ECG data"""
        try:
            query = self.session.query(self.model).filter(
                self.model.ecg_mat.isnot(None)
            ).order_by(self.model.visit_date.desc())
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting visits with ECG: {str(e)}")
    
    def get_visits_with_pending_payment(self) -> List[Visit]:
        """Get visits with unpaid or partial payment status"""
        try:
            query = self.session.query(self.model).filter(
                self.model.payment_status.in_(["unpaid", "partial"])
            ).order_by(self.model.visit_date.desc())
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting visits with pending payment: {str(e)}")
    
    def get_visits_needing_followup(self) -> List[Visit]:
        """Get visits that have follow-up dates in the future"""
        try:
            now = datetime.now()
            query = self.session.query(self.model).filter(
                and_(
                    self.model.follow_up_date.isnot(None),
                    self.model.follow_up_date >= now
                )
            ).order_by(self.model.follow_up_date)
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting visits needing follow-up: {str(e)}")
    
    def get_overdue_followups(self) -> List[Visit]:
        """Get visits with overdue follow-up dates"""
        try:
            now = datetime.now()
            query = self.session.query(self.model).filter(
                and_(
                    self.model.follow_up_date.isnot(None),
                    self.model.follow_up_date < now
                )
            ).order_by(self.model.follow_up_date)
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting overdue follow-ups: {str(e)}")
    
    def get_visit_by_appointment(self, appointment_id: int) -> Optional[Visit]:
        """Get visit by appointment ID"""
        return self.get_by_field("appointment_id", appointment_id)
    
    def get_total_revenue_by_date_range(self, start_date: date, end_date: date) -> float:
        """Get total revenue from visits in date range"""
        try:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
            
            result = self.session.query(func.sum(self.model.payment_total)).filter(
                and_(
                    self.model.visit_date >= start_datetime,
                    self.model.visit_date <= end_datetime,
                    self.model.payment_status == "paid"
                )
            ).scalar()
            
            return float(result or 0)
        except Exception as e:
            raise Exception(f"Error calculating total revenue: {str(e)}")
