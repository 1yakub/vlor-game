"""Configuration management for the game.

This module handles loading and validating environment variables using Pydantic.
It provides type-safe access to configuration values throughout the application.
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    Attributes:
        SERVER_HOST: Host address for the server
        SERVER_PORT: Port number for the server
        DEBUG: Debug mode flag
        DATABASE_URL: Database connection string
        MAX_PLAYERS_PER_ROOM: Maximum number of players in a game room
        TICK_RATE: Game update rate in Hz
        PLAYER_MOVE_SPEED: Base movement speed for players
        SOCKET_IO_PATH: Socket.IO endpoint path
        CLIENT_UPDATE_RATE: Client update frequency in Hz
        SERVER_UPDATE_RATE: Server update frequency in Hz
        SECRET_KEY: Secret key for JWT encoding
        JWT_ALGORITHM: Algorithm used for JWT
        ACCESS_TOKEN_EXPIRE_MINUTES: JWT token expiration time
        LOG_LEVEL: Logging level
        LOG_FILE: Log file path
    """
    
    # Server Configuration
    SERVER_HOST: str = Field(default="localhost")
    SERVER_PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    
    # Database Configuration
    DATABASE_URL: str = Field(default="sqlite:///./vlor.db")
    
    # Game Configuration
    MAX_PLAYERS_PER_ROOM: int = Field(default=10)
    TICK_RATE: int = Field(default=60)
    PLAYER_MOVE_SPEED: float = Field(default=5.0)
    
    # Networking
    SOCKET_IO_PATH: str = Field(default="/socket.io")
    CLIENT_UPDATE_RATE: int = Field(default=60)
    SERVER_UPDATE_RATE: int = Field(default=20)
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-here")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Logging
    LOG_LEVEL: str = Field(default="DEBUG")
    LOG_FILE: str = Field(default="vlor.log")
    
    class Config:
        """Pydantic configuration class."""
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the application settings.
    
    Returns:
        Settings: Application configuration instance
    """
    return settings 