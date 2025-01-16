"""Basic tests to verify project setup.

These tests ensure that the project is set up correctly and all
core functionality is working as expected.
"""

import os
import pytest
from pathlib import Path
from src.shared.config import settings
from src.shared.logger import get_logger
from src.shared.errors import GameError

logger = get_logger(__name__)

def test_project_structure():
    """Test that all required directories exist."""
    required_dirs = [
        "assets/sprites",
        "assets/sounds",
        "assets/maps",
        "src/client",
        "src/server",
        "src/shared",
        "tests"
    ]
    
    for directory in required_dirs:
        path = Path(directory)
        assert path.exists(), f"Directory {directory} does not exist"
        assert path.is_dir(), f"{directory} is not a directory"

def test_environment_variables():
    """Test that environment variables are loaded correctly."""
    assert hasattr(settings, "SERVER_HOST"), "SERVER_HOST not found in settings"
    assert hasattr(settings, "SERVER_PORT"), "SERVER_PORT not found in settings"
    assert hasattr(settings, "DATABASE_URL"), "DATABASE_URL not found in settings"

def test_logging_setup():
    """Test that logging is configured correctly."""
    test_logger = get_logger("test")
    assert test_logger is not None, "Logger not created"
    assert test_logger.level == settings.LOG_LEVEL.upper(), "Incorrect log level"

def test_error_handling():
    """Test custom error handling."""
    with pytest.raises(GameError) as exc_info:
        raise GameError(
            message="Test error",
            context={"test": True},
            error_code="TEST_ERROR"
        )
    
    assert exc_info.value.message == "Test error"
    assert exc_info.value.context == {"test": True}
    assert exc_info.value.error_code == "TEST_ERROR"

@pytest.mark.network
def test_network_imports():
    """Test that network-related packages are installed."""
    try:
        import socketio
        import fastapi
        import uvicorn
    except ImportError as e:
        pytest.fail(f"Network package import failed: {e}")

@pytest.mark.pygame
def test_pygame_setup():
    """Test that Pygame is installed and can be initialized."""
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((100, 100))
        pygame.display.quit()
    except Exception as e:
        pytest.fail(f"Pygame initialization failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__]) 