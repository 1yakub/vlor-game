"""Player module for handling the player entity."""

import pygame
from pygame.math import Vector2

from shared.constants import (
    PLAYER_SIZE,
    PLAYER_SPEED,
    COLOR_BLACK,
    PlayerRole
)
from client.sprites import SpriteManager, Direction, AnimationState

class Player:
    """Player entity class.
    
    Attributes:
        position: Current position in world coordinates
        velocity: Current movement velocity
        rect: Collision rectangle
        role: Player's role in the game
        direction: Current facing direction
        state: Current animation state
        sprite_manager: Handles sprite animations
    """
    
    def __init__(
        self,
        position: Vector2,
        role: PlayerRole = PlayerRole.MEDIATOR_RUPOK,
        color: tuple[int, int, int] = COLOR_BLACK
    ):
        """Initialize the player.
        
        Args:
            position: Starting position
            role: Player's role
            color: Fallback color if sprites fail to load
        """
        self.position = position
        self.velocity = Vector2(0, 0)
        self.role = role
        self.color = color
        
        # Create collision rectangle
        self.rect = pygame.Rect(
            position.x - PLAYER_SIZE // 2,
            position.y - PLAYER_SIZE // 2,
            PLAYER_SIZE,
            PLAYER_SIZE
        )
        
        # Animation state
        self.direction = Direction.DOWN
        self.state = AnimationState.IDLE
        self.sprite_manager = SpriteManager()
    
    def handle_input(self, keys: dict) -> None:
        """Handle keyboard input for movement.
        
        Args:
            keys: Dictionary of keyboard state
        """
        # Reset velocity
        self.velocity = Vector2(0, 0)
        
        # Handle movement keys and update direction
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
            self.direction = Direction.LEFT
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
            self.direction = Direction.RIGHT
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -PLAYER_SPEED
            self.direction = Direction.UP
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = PLAYER_SPEED
            self.direction = Direction.DOWN
            
        # Normalize diagonal movement
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * PLAYER_SPEED
            self.state = AnimationState.WALKING
        else:
            self.state = AnimationState.IDLE
    
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
        # Get current animation frame
        sprite = self.sprite_manager.get_sprite_frame(
            self.role,
            self.direction,
            self.state,
            pygame.time.get_ticks() / 1000.0
        )
        
        # Draw sprite centered on position
        sprite_rect = sprite.get_rect(center=self.position)
        screen.blit(sprite, sprite_rect) 