"""Player module.

This module handles player-related functionality including movement,
rendering, and state management.
"""

from typing import Optional, Tuple
import pygame
from pygame.math import Vector2
from shared.constants import (
    PLAYER_SIZE,
    PLAYER_SPEED,
    COLOR_BLACK,
    WINDOW_WIDTH,
    WINDOW_HEIGHT
)

class Player:
    """Player class representing a game character.
    
    Attributes:
        position: Current position in the game world
        velocity: Current movement velocity
        sprite: Player's visual representation (optional)
    """
    
    def __init__(
        self,
        position: Vector2,
        sprite_path: Optional[str] = None,
        color: Tuple[int, int, int] = COLOR_BLACK
    ):
        """Initialize the player.
        
        Args:
            position: Starting position
            sprite_path: Path to sprite image (optional)
            color: Fallback color if no sprite is provided
        """
        self.position = position
        self.velocity = Vector2(0, 0)
        self.color = color
        self.sprite = None
        self.rect = pygame.Rect(
            position.x - PLAYER_SIZE.x // 2,
            position.y - PLAYER_SIZE.y // 2,
            PLAYER_SIZE.x,
            PLAYER_SIZE.y
        )
        
        if sprite_path:
            self._load_sprite(sprite_path)
    
    def _load_sprite(self, sprite_path: str) -> None:
        """Load the player sprite from file.
        
        Args:
            sprite_path: Path to sprite image
        """
        try:
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, PLAYER_SIZE)
        except pygame.error as e:
            print(f"Could not load sprite: {e}")
    
    def handle_input(self, keys) -> None:
        """Handle keyboard input for player movement.
        
        Args:
            keys: Pygame key state dictionary
        """
        self.velocity = Vector2(0, 0)
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = 1
        
        # Normalize velocity for consistent movement speed
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * PLAYER_SPEED
    
    def update(self, delta_time: float) -> None:
        """Update player state.
        
        Args:
            delta_time: Time elapsed since last update
        """
        # Update position
        movement = self.velocity * delta_time
        new_pos = self.position + movement
        
        # Keep player within screen bounds
        new_pos.x = max(PLAYER_SIZE.x // 2, min(new_pos.x, WINDOW_WIDTH - PLAYER_SIZE.x // 2))
        new_pos.y = max(PLAYER_SIZE.y // 2, min(new_pos.y, WINDOW_HEIGHT - PLAYER_SIZE.y // 2))
        
        self.position = new_pos
        self.rect.center = self.position
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player to the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        if self.sprite:
            screen.blit(self.sprite, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect) 