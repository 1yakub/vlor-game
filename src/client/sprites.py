"""Sprite management system for handling game animations."""

from enum import Enum, auto
from typing import Dict, List, Optional
import pygame
from pygame.math import Vector2

from shared.constants import (
    PLAYER_SIZE,
    SPRITE_PATH,
    ANIMATION_FRAME_RATE,
    PlayerRole
)
from shared.logger import get_logger

logger = get_logger(__name__)

class Direction(Enum):
    """Character facing directions."""
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()

class AnimationState(Enum):
    """Character animation states."""
    IDLE = auto()
    WALKING = auto()

class SpriteManager:
    """Manages character sprites and animations.
    
    Attributes:
        sprites: Dictionary of sprite sheets for each role
        current_frame: Current animation frame index
        animation_timer: Time accumulator for animation
        frame_duration: Time between animation frames
    """
    
    def __init__(self):
        """Initialize the sprite manager."""
        self.sprites: Dict[PlayerRole, pygame.Surface] = {}
        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 1.0 / ANIMATION_FRAME_RATE
        
        # Load sprite sheets for each role
        self._load_sprites()
    
    def _load_sprites(self) -> None:
        """Load sprite sheets for all player roles."""
        sprite_paths = {
            PlayerRole.MEDIATOR_RUPOK: SPRITE_PATH / "rupok.png",
            PlayerRole.MEDIATOR_SHORON: SPRITE_PATH / "shoron.png",
            PlayerRole.BUSINESSMAN: SPRITE_PATH / "businessman.png",
            PlayerRole.MAFIA: SPRITE_PATH / "mafia.png"
        }
        
        for role, path in sprite_paths.items():
            try:
                if path.exists():
                    sprite_sheet = pygame.image.load(str(path)).convert_alpha()
                    self.sprites[role] = sprite_sheet
                else:
                    logger.warning(f"Sprite file not found for {role}: {path}")
                    fallback = self._create_fallback_sprite(role)
                    self.sprites[role] = fallback
            except (pygame.error, IOError) as e:
                logger.error(f"Error loading sprite for {role}: {e}")
                fallback = self._create_fallback_sprite(role)
                self.sprites[role] = fallback
    
    def _create_fallback_sprite(self, role: PlayerRole) -> pygame.Surface:
        """Create a fallback sprite when image loading fails.
        
        Args:
            role: Player role to create fallback for
            
        Returns:
            Surface with role-specific color
        """
        colors = {
            PlayerRole.MEDIATOR_RUPOK: (0, 255, 0),  # Green
            PlayerRole.MEDIATOR_SHORON: (0, 0, 255),  # Blue
            PlayerRole.BUSINESSMAN: (255, 215, 0),  # Gold
            PlayerRole.MAFIA: (255, 0, 0)  # Red
        }
        
        # Create surface for sprite sheet (4 directions x 4 frames)
        surface = pygame.Surface((PLAYER_SIZE * 4, PLAYER_SIZE * 4), pygame.SRCALPHA)
        color = colors.get(role, (128, 128, 128))  # Gray as default
        
        # Draw colored rectangles for each frame
        for y in range(4):  # 4 directions
            for x in range(4):  # 4 frames per direction
                rect = pygame.Rect(
                    x * PLAYER_SIZE,
                    y * PLAYER_SIZE,
                    PLAYER_SIZE,
                    PLAYER_SIZE
                )
                pygame.draw.rect(surface, color, rect)
        
        return surface
    
    def get_sprite_frame(
        self,
        role: PlayerRole,
        direction: Direction,
        state: AnimationState,
        delta_time: float
    ) -> pygame.Surface:
        """Get the current sprite frame for a character.
        
        Args:
            role: Character's role
            direction: Facing direction
            state: Current animation state
            delta_time: Time elapsed since last frame
            
        Returns:
            Current frame of the sprite animation
        """
        sprite_sheet = self.sprites[role]
        
        # Update animation timer
        self.animation_timer += delta_time
        if self.animation_timer >= self.frame_duration:
            self.animation_timer -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % 4
        
        # Calculate frame position in sprite sheet
        direction_row = {
            Direction.DOWN: 0,
            Direction.LEFT: 1,
            Direction.RIGHT: 2,
            Direction.UP: 3
        }[direction]
        
        # If idle, use first frame
        if state == AnimationState.IDLE:
            self.current_frame = 0
        
        # Extract frame from sprite sheet
        frame_rect = pygame.Rect(
            self.current_frame * PLAYER_SIZE,
            direction_row * PLAYER_SIZE,
            PLAYER_SIZE,
            PLAYER_SIZE
        )
        
        frame = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), frame_rect)
        
        return frame 