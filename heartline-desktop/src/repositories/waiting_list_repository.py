"""
Waiting List Repository for Heartline Desktop Application

This module provides data access methods for WaitingListEntry entities.
"""

from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import and_, or_, func

from .base import BaseRepository
from ..models.complete_models import WaitingListEntry

class WaitingListRepository(BaseRepository[WaitingListEntry]):
    """Repository for WaitingListEntry entities"""
    
    def __init__(self):
        super().__init__(WaitingListEntry)
    
    def get_current_queue(self) -> List[WaitingListEntry]:
        """Get current waiting list ordered by priority and arrival time"""
        try:
            query = self.session.query(self.model).filter(
                self.model.status.in_(["waiting", "called"])
            ).order_by(
                self.model.priority.desc(),
                self.model.arrival_time.asc()
            )
            
            return query.all()
        except Exception as e:
            raise Exception(f"Error getting current queue: {str(e)}")
    
    def get_waiting_patients(self) -> List[WaitingListEntry]:
        """Get patients currently waiting"""
        return self.get_many_by_field("status", "waiting")
    
    def get_called_patients(self) -> List[WaitingListEntry]:
        """Get patients that have been called"""
        return self.get_many_by_field("status", "called")
    
    def get_in_progress_patients(self) -> List[WaitingListEntry]:
        """Get patients currently in progress"""
        return self.get_many_by_field("status", "in_progress")
    
    def get_queue_by_doctor(self, doctor_id: int) -> List[WaitingListEntry]:
        """Get waiting list for specific doctor"""
        return self.get_many_by_field("assigned_doctor", doctor_id)
    
    def get_queue_position(self, entry_id: int) -> int:
        """Get position of entry in the queue"""
        try:
            entry = self.get_by_id(entry_id)
            if not entry or entry.status not in ["waiting", "called"]:
                return 0
            
            count = self.session.query(self.model).filter(
                and_(
                    self.model.status.in_(["waiting", "called"]),
                    self.model.id != entry_id,
                    # Higher priority or same priority but earlier arrival
                    or_(
                        self.model.priority > entry.priority,
                        and_(
                            self.model.priority == entry.priority,
                            self.model.arrival_time < entry.arrival_time
                        )
                    )
                )
            ).count()
            
            return count + 1
        except Exception as e:
            raise Exception(f"Error getting queue position: {str(e)}")
    
    def get_average_wait_time(self, doctor_id: Optional[int] = None) -> float:
        """Get average wait time in minutes"""
        try:
            query = self.session.query(self.model).filter(
                self.model.status == "in_progress"
            )
            
            if doctor_id:
                query = query.filter(self.model.assigned_doctor == doctor_id)
            
            entries = query.all()
            if not entries:
                return 0.0
            
            total_wait_time = 0
            for entry in entries:
                wait_time = (datetime.utcnow() - entry.arrival_time).total_seconds() / 60
                total_wait_time += wait_time
            
            return total_wait_time / len(entries)
        except Exception as e:
            raise Exception(f"Error calculating average wait time: {str(e)}")
    
    def get_next_patient(self, doctor_id: Optional[int] = None) -> Optional[WaitingListEntry]:
        """Get next patient in queue"""
        try:
            query = self.session.query(self.model).filter(
                self.model.status == "waiting"
            )
            
            if doctor_id:
                query = query.filter(
                    or_(
                        self.model.assigned_doctor == doctor_id,
                        self.model.assigned_doctor.is_(None)
                    )
                )
            
            entry = query.order_by(
                self.model.priority.desc(),
                self.model.arrival_time.asc()
            ).first()
            
            return entry
        except Exception as e:
            raise Exception(f"Error getting next patient: {str(e)}")
    
    def add_patient_to_queue(self, patient_id: int, priority: int = 5, 
                           doctor_id: Optional[int] = None) -> WaitingListEntry:
        """Add patient to waiting list"""
        return self.create(
            patient_id=patient_id,
            priority=priority,
            assigned_doctor=doctor_id,
            status="waiting"
        )
    
    def call_next_patient(self, doctor_id: Optional[int] = None) -> Optional[WaitingListEntry]:
        """Call next patient in queue"""
        try:
            next_patient = self.get_next_patient(doctor_id)
            if next_patient:
                updated = self.update(next_patient.id, status="called")
                return updated
            return None
        except Exception as e:
            raise Exception(f"Error calling next patient: {str(e)}")
    
    def mark_patient_in_progress(self, entry_id: int) -> Optional[WaitingListEntry]:
        """Mark patient as in progress"""
        return self.update(entry_id, status="in_progress")
    
    def complete_patient_visit(self, entry_id: int) -> bool:
        """Remove patient from queue (visit completed)"""
        return self.delete(entry_id)
    
    def skip_patient(self, entry_id: int) -> Optional[WaitingListEntry]:
        """Mark patient as skipped"""
        return self.update(entry_id, status="skipped")
