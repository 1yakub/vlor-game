"""Player module.

This module handles the player character and its interactions.
"""

import pygame
from pygame.math import Vector2

from shared.constants import (
    PLAYER_SIZE,
    PLAYER_SPEED,
    COLOR_BLACK,
    PlayerRole,
    STARTING_MONEY
)
from shared.logger import get_logger
from client.sprites import SpriteManager, Direction, AnimationState

logger = get_logger(__name__)

class Player:
    """Player class representing the user's character."""
    
    def __init__(self, position: Vector2, name: str = "Player"):
        """Initialize the player.
        
        Args:
            position: Starting position
            name: Player name
        """
        self.name = name
        self.position = position
        self.velocity = Vector2(0, 0)
        self.money = STARTING_MONEY
        
        # Create sprite manager
        self.sprite_manager = SpriteManager()
        
        # Create collision rect
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.rect.center = self.position
        
        logger.info(f"Created player: {self.name}")
    
    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handle keyboard input.
        
        Args:
            keys: Pressed keys
        """
        # Reset velocity
        self.velocity = Vector2(0, 0)
        
        # Movement
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity.y = -PLAYER_SPEED
            self.sprite_manager.set_direction(Direction.UP)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity.y = PLAYER_SPEED
            self.sprite_manager.set_direction(Direction.DOWN)
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity.x = -PLAYER_SPEED
            self.sprite_manager.set_direction(Direction.LEFT)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity.x = PLAYER_SPEED
            self.sprite_manager.set_direction(Direction.RIGHT)
        
        # Update animation state
        if self.velocity.length() > 0:
            self.sprite_manager.set_state(AnimationState.WALKING)
        else:
            self.sprite_manager.set_state(AnimationState.IDLE)
    
    def update(self, delta_time: float) -> None:
        """Update player state.
        
        Args:
            delta_time: Time elapsed since last update
        """
        # Update position
        self.position += self.velocity * delta_time
        self.rect.center = self.position
        
        # Update sprite animation
        self.sprite_manager.update(delta_time)
    
    def draw(self, screen: pygame.Surface, screen_pos: pygame.Vector2) -> None:
        """Draw the player.
        
        Args:
            screen: Surface to draw on
            screen_pos: Position on screen (camera-relative)
        """
        sprite = self.sprite_manager.get_current_sprite()
        if sprite:
            screen.blit(sprite, (screen_pos.x - PLAYER_SIZE // 2, screen_pos.y - PLAYER_SIZE // 2))
        else:
            # Fallback to rectangle if sprite not found
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(
                screen_pos.x - PLAYER_SIZE // 2,
                screen_pos.y - PLAYER_SIZE // 2,
                PLAYER_SIZE,
                PLAYER_SIZE
            ))
    
    def add_money(self, amount: float) -> None:
        """Add money to the player.
        
        Args:
            amount: Amount to add
        """
        self.money += amount
        logger.debug(f"{self.name} added ${amount:,.2f}")
    
    def remove_money(self, amount: float) -> bool:
        """Remove money from the player.
        
        Args:
            amount: Amount to remove
        
        Returns:
            True if money was removed, False if insufficient funds
        """
        if self.money < amount:
            return False
        
        self.money -= amount
        logger.debug(f"{self.name} removed ${amount:,.2f}")
        return True 