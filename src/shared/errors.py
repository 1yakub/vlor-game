"""Error handling for the game.

This module defines custom exceptions and error handling utilities.
It provides consistent error handling throughout the application.
"""

from typing import Optional, Dict, Any
from .logger import logger


class GameError(Exception):
    """Base class for game-specific exceptions.
    
    Attributes:
        message: Error message
        context: Additional context about the error
        error_code: Unique error code for identification
    """
    
    def __init__(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None
    ) -> None:
        self.message = message
        self.context = context or {}
        self.error_code = error_code
        
        # Log the error
        logger.error(
            f"GameError: {message} | Code: {error_code} | Context: {context}"
        )
        
        super().__init__(self.message)


class NetworkError(GameError):
    """Raised when a networking operation fails."""
    pass


class StateError(GameError):
    """Raised when an invalid game state is encountered."""
    pass


class AuthenticationError(GameError):
    """Raised when authentication fails."""
    pass


class ValidationError(GameError):
    """Raised when input validation fails."""
    pass


class ResourceError(GameError):
    """Raised when a resource operation fails."""
    pass


def handle_error(error: Exception) -> Dict[str, Any]:
    """Convert an exception into a standardized error response.
    
    Args:
        error: The exception to handle
        
    Returns:
        Dict containing error details
    """
    if isinstance(error, GameError):
        return {
            "error": error.message,
            "error_code": error.error_code,
            "context": error.context
        }
    
    # Handle unexpected errors
    logger.exception("Unexpected error occurred")
    return {
        "error": "An unexpected error occurred",
        "error_code": "INTERNAL_ERROR",
        "context": {"type": str(type(error)), "message": str(error)}
    } 