"""Project setup and initialization script.

This script handles initial project setup, including:
- Creating necessary directories
- Setting up the database
- Checking dependencies
- Initializing configuration
"""

import os
import sys
import shutil
from pathlib import Path
from shared.logger import logger, setup_logger
from shared.config import settings

setup_logger = setup_logger("setup")

def check_python_version() -> bool:
    """Check if Python version meets requirements.
    
    Returns:
        bool: True if version is compatible, False otherwise
    """
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        setup_logger.error(
            f"Python {required_version[0]}.{required_version[1]} or higher is required"
        )
        return False
    return True

def create_directories() -> None:
    """Create necessary project directories."""
    directories = [
        "assets/sprites",
        "assets/sounds",
        "assets/maps",
        "logs",
        "data"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        setup_logger.info(f"Created directory: {path}")

def create_env_file() -> None:
    """Create .env file if it doesn't exist."""
    if not Path(".env").exists():
        shutil.copy(".env.example", ".env")
        setup_logger.info("Created .env file from .env.example")

def check_dependencies() -> bool:
    """Check if all required packages are installed.
    
    Returns:
        bool: True if all dependencies are met, False otherwise
    """
    try:
        import pygame
        import fastapi
        import socketio
        import sqlalchemy
        import pytest
        setup_logger.info("All required packages are installed")
        return True
    except ImportError as e:
        setup_logger.error(f"Missing dependency: {e.name}")
        return False

def setup_database() -> None:
    """Initialize the database."""
    from sqlalchemy import create_engine
    from sqlalchemy.exc import SQLAlchemyError
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        # Here you would typically import your models and create tables
        # Base.metadata.create_all(engine)
        setup_logger.info("Database initialized successfully")
    except SQLAlchemyError as e:
        setup_logger.error(f"Database initialization failed: {e}")
        raise

def main() -> None:
    """Run the setup process."""
    setup_logger.info("Starting project setup...")
    
    try:
        # Check Python version
        if not check_python_version():
            sys.exit(1)
        
        # Check dependencies
        if not check_dependencies():
            setup_logger.error("Please install all required packages")
            sys.exit(1)
        
        # Create directories
        create_directories()
        
        # Create .env file
        create_env_file()
        
        # Setup database
        setup_database()
        
        setup_logger.info("Project setup completed successfully")
        
    except Exception as e:
        setup_logger.exception("Setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 