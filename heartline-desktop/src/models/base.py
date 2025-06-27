"""
Base model for all database entities

This module provides the base model class that matches the web app structure.
Only provides the declarative base, individual models define their own fields.
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
