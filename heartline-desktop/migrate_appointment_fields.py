"""
Database Migration Script - Add Enhanced Appointment Columns

This script adds the missing appointment fields to the database to match our enhanced model.
Run this script to synchronize the database with the enhanced appointment functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import db_manager
from sqlalchemy import text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_appointment_table():
    """Add missing columns to the appointment table"""
    
    # List of columns to add with their SQL definitions
    new_columns = [
        ("appointment_type", "VARCHAR(50) DEFAULT 'consultation'"),
        ("duration_minutes", "INTEGER DEFAULT 30"),
        ("priority", "VARCHAR(20) DEFAULT 'normal'"),
        ("notes", "TEXT"),
        ("patient_notes", "TEXT"),
        ("confirmed", "BOOLEAN DEFAULT FALSE"),
        ("reminder_sent", "BOOLEAN DEFAULT FALSE"),
        ("cancelled_reason", "VARCHAR(200)"),
        ("cancelled_by", "VARCHAR(50)"),
        ("rescheduled_from", "INTEGER REFERENCES appointment(id)")
    ]
    
    try:
        with db_manager.get_session() as session:
            # Check which columns already exist
            result = session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'appointment' 
                AND table_schema = 'public'
            """))
            
            existing_columns = {row[0] for row in result.fetchall()}
            logger.info(f"Existing columns: {existing_columns}")
            
            # Add missing columns
            for column_name, column_definition in new_columns:
                if column_name not in existing_columns:
                    logger.info(f"Adding column: {column_name}")
                    
                    sql = f"ALTER TABLE appointment ADD COLUMN {column_name} {column_definition}"
                    logger.info(f"Executing: {sql}")
                    
                    session.execute(text(sql))
                    session.commit()
                    
                    logger.info(f"✅ Added column: {column_name}")
                else:
                    logger.info(f"⏭️ Column {column_name} already exists, skipping")
            
            logger.info("🎉 Migration completed successfully!")
            
            # Verify the new structure
            result = session.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'appointment' 
                AND table_schema = 'public'
                ORDER BY ordinal_position
            """))
            
            print("\n📋 Updated appointment table structure:")
            print("Column Name | Data Type | Nullable | Default")
            print("-" * 50)
            for row in result.fetchall():
                nullable = "YES" if row[2] == "YES" else "NO"
                default = row[3] if row[3] else "None"
                print(f"{row[0]:<20} | {row[1]:<12} | {nullable:<8} | {default}")
                
    except Exception as e:
        logger.error(f"❌ Migration failed: {str(e)}")
        raise

def verify_migration():
    """Verify that all columns exist and can be used"""
    try:
        from src.models.complete_models import Appointment
        
        with db_manager.get_session() as session:
            # Try to query with the new fields
            appointment = session.query(Appointment).first()
            if appointment:
                logger.info("✅ Model can successfully query enhanced fields")
                logger.info(f"Sample appointment: ID={appointment.id}, Type={appointment.appointment_type}")
            else:
                logger.info("ℹ️ No appointments found to test with")
                
    except Exception as e:
        logger.error(f"❌ Verification failed: {str(e)}")
        raise

if __name__ == "__main__":
    print("🚀 Starting Appointment Table Migration...")
    print("This will add enhanced fields to the appointment table.")
    
    try:
        # Initialize database connection
        db_manager.initialize()
        
        # Run migration
        migrate_appointment_table()
        
        # Verify migration
        verify_migration()
        
        print("\n✅ Migration completed successfully!")
        print("The appointment table now supports all enhanced features.")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        print("Please check the error and try again.")
        sys.exit(1)
