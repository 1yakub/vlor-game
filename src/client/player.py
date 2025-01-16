"""Player module for handling the player entity."""

import pygame
from pygame.math import Vector2

from shared.constants import (
    PLAYER_SIZE,
    PLAYER_SPEED,
    COLOR_BLACK
)

class Player:
    """Player entity class.
    
    Attributes:
        position: Current position in world coordinates
        velocity: Current movement velocity
        rect: Collision rectangle
        color: Player color (temporary until sprites)
    """
    
    def __init__(
        self,
        position: Vector2,
        color: tuple[int, int, int] = COLOR_BLACK
    ):
        """Initialize the player.
        
        Args:
            position: Starting position
            color: RGB color tuple
        """
        self.position = position
        self.velocity = Vector2(0, 0)
        self.color = color
        
        # Create collision rectangle
        self.rect = pygame.Rect(
            position.x - PLAYER_SIZE // 2,
            position.y - PLAYER_SIZE // 2,
            PLAYER_SIZE,
            PLAYER_SIZE
        )
    
    def handle_input(self, keys: dict) -> None:
        """Handle keyboard input for movement.
        
        Args:
            keys: Dictionary of keyboard state
        """
        # Reset velocity
        self.velocity = Vector2(0, 0)
        
        # Handle movement keys
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = PLAYER_SPEED
            
        # Normalize diagonal movement
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * PLAYER_SPEED
    
    def update(self, delta_time: float) -> None:
        """Update player state.
        
        Args:
            delta_time: Time elapsed since last update
        """
        # Update position based on velocity
        self.position += self.velocity * delta_time
        
        # Update collision rect
        self.rect.center = self.position
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player.
        
        Args:
            screen: Surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect) 