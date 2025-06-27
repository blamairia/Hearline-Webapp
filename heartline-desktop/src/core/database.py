"""
Database Management for Heartline Desktop Application

This module handles all database operations including:
- Connection management with pooling
- Session management with automatic cleanup
- Transaction handling
- Database initialization
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Optional, Generator
import logging

from .config import config
from ..models.base import Base
# Import all models to ensure they're registered with SQLAlchemy
from ..models.complete_models import *

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database manager with connection pooling and session management"""
    
    def __init__(self):
        self.engine: Optional[object] = None
        self.SessionLocal: Optional[sessionmaker] = None
        self._initialized = False
        
    def initialize(self) -> bool:
        """Initialize database connection"""
        if self._initialized:
            return True
            
        try:
            # Create engine with connection pooling
            # For local development, don't require SSL
            connect_args = {}
            if config.DB_HOST != "localhost" and not config.DEBUG:
                connect_args = {"sslmode": "require"}
                
            self.engine = create_engine(
                config.database_url,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
                echo=config.DEBUG,
                connect_args=connect_args
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            # Create tables if they don't exist
            Base.metadata.create_all(bind=self.engine)
                
            logger.info("Database connection established successfully")
            self._initialized = True
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"Database initialization failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during database initialization: {e}")
            return False
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get database session with automatic cleanup"""
        if not self._initialized:
            raise RuntimeError("Database not initialized. Call initialize() first.")
            
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def create_tables(self):
        """Create all database tables"""
        try:
            if not self._initialized:
                raise RuntimeError("Database not initialized")
                
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    def check_connection(self) -> bool:
        """Check if database connection is alive"""
        try:
            if not self._initialized or not self.engine:
                return False
                
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
    
    def close(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()
            self._initialized = False
            logger.info("Database connections closed")

# Global database manager instance
db_manager = DatabaseManager()
