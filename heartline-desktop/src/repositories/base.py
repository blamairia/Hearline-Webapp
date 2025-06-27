"""
Base Repository for Heartline Desktop Application

This module provides the base repository class with common CRUD operations
that all other repositories inherit from.
"""

from typing import List, Optional, TypeVar, Generic, Type, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from ..core.database import db_manager
from ..core.exceptions import DatabaseError

logger = logging.getLogger(__name__)

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    def create(self, **kwargs) -> T:
        """Create a new entity"""
        try:
            with db_manager.get_session() as session:
                entity = self.model_class(**kwargs)
                session.add(entity)
                session.flush()
                session.refresh(entity)
                return entity
        except SQLAlchemyError as e:
            logger.error(f"Failed to create {self.model_class.__name__}: {e}")
            raise DatabaseError(f"Create operation failed: {e}")
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID"""
        try:
            with db_manager.get_session() as session:
                return session.query(self.model_class).filter(
                    self.model_class.id == entity_id
                ).first()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get {self.model_class.__name__} by ID: {e}")
            raise DatabaseError(f"Get operation failed: {e}")
    
    def get_all(self, active_only: bool = True) -> List[T]:
        """Get all entities"""
        try:
            with db_manager.get_session() as session:
                query = session.query(self.model_class)
                if active_only and hasattr(self.model_class, 'is_active'):
                    query = query.filter(self.model_class.is_active == True)
                return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get all {self.model_class.__name__}: {e}")
            raise DatabaseError(f"Get all operation failed: {e}")
    
    def update(self, entity_id: int, **kwargs) -> Optional[T]:
        """Update entity by ID"""
        try:
            with db_manager.get_session() as session:
                entity = session.query(self.model_class).filter(
                    self.model_class.id == entity_id
                ).first()
                
                if entity:
                    for key, value in kwargs.items():
                        if hasattr(entity, key):
                            setattr(entity, key, value)
                    session.flush()
                    session.refresh(entity)
                
                return entity
        except SQLAlchemyError as e:
            logger.error(f"Failed to update {self.model_class.__name__}: {e}")
            raise DatabaseError(f"Update operation failed: {e}")
    
    def delete(self, entity_id: int) -> bool:
        """Soft delete entity by ID"""
        try:
            with db_manager.get_session() as session:
                entity = session.query(self.model_class).filter(
                    self.model_class.id == entity_id
                ).first()
                
                if entity:
                    if hasattr(entity, 'is_active'):
                        entity.is_active = False
                    else:
                        session.delete(entity)
                    return True
                
                return False
        except SQLAlchemyError as e:
            logger.error(f"Failed to delete {self.model_class.__name__}: {e}")
            raise DatabaseError(f"Delete operation failed: {e}")
    
    def count(self, active_only: bool = True) -> int:
        """Count entities"""
        try:
            with db_manager.get_session() as session:
                query = session.query(self.model_class)
                if active_only and hasattr(self.model_class, 'is_active'):
                    query = query.filter(self.model_class.is_active == True)
                return query.count()
        except SQLAlchemyError as e:
            logger.error(f"Failed to count {self.model_class.__name__}: {e}")
            raise DatabaseError(f"Count operation failed: {e}")
    
    def search(self, **filters) -> List[T]:
        """Search entities with filters"""
        try:
            with db_manager.get_session() as session:
                query = session.query(self.model_class)
                
                for key, value in filters.items():
                    if hasattr(self.model_class, key):
                        query = query.filter(getattr(self.model_class, key) == value)
                
                return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Failed to search {self.model_class.__name__}: {e}")
            raise DatabaseError(f"Search operation failed: {e}")
