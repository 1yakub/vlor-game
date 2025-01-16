"""Main game module.

This module contains the core game engine and main game loop.
"""

import sys
from pathlib import Path
import pygame
import pygame_gui
from pygame.math import Vector2

from shared.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    COLOR_WHITE,
    COLOR_BLACK,
    GameState,
    ASSET_DIR
)
from shared.logger import get_logger
from client.player import Player
from client.tilemap import create_test_map
from client.ui.menu import MenuManager

logger = get_logger(__name__)

class Game:
    """Main game class handling the game loop and core functionality."""
    
    def __init__(self):
        """Initialize the game engine and create the game window."""
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        
        # Set up the display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        
        # Create UI manager with theme
        theme_path = ASSET_DIR / "theme.json"
        try:
            if theme_path.exists():
                logger.info(f"Loading UI theme from {theme_path}")
                self.ui_manager = pygame_gui.UIManager(
                    (WINDOW_WIDTH, WINDOW_HEIGHT),
                    str(theme_path)
                )
            else:
                logger.warning(f"Theme file not found: {theme_path}, using default theme")
                self.ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            logger.error(f"Error loading theme: {e}, using default theme")
            self.ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Game state
        self.state = GameState.MENU
        
        # Create menu manager
        self.menu_manager = MenuManager(self.ui_manager)
        
        # Create tilemap
        self.tilemap = create_test_map()
        
        # Create player at center of screen
        self.player = Player(
            position=Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        
        logger.info("Game initialized successfully")
    
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            # Handle UI events
            self.ui_manager.process_events(event)
            self.menu_manager.handle_event(event)
            
            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                        self.menu_manager.show_state(GameState.PAUSED)
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                        self.menu_manager.show_state(GameState.PLAYING)
    
    def update(self, delta_time: float):
        """Update game state.
        
        Args:
            delta_time: Time elapsed since last update in seconds
        """
        # Update UI
        self.ui_manager.update(delta_time)
        
        # Only update game logic when playing
        if self.state == GameState.PLAYING:
            # Store old position for collision checking
            old_pos = self.player.position.copy()
            
            # Handle player input and update
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            self.player.update(delta_time)
            
            # Check for collisions with tilemap
            if self.tilemap.check_collision(self.player.rect):
                # If collision occurred, revert to old position
                self.player.position = old_pos
                self.player.rect.center = old_pos
            
            # Log room changes for debugging
            current_room = self.tilemap.get_room_at(self.player.position)
            if hasattr(self, '_last_room') and self._last_room != current_room:
                if current_room:
                    logger.debug(f"Entered room: {current_room}")
                else:
                    logger.debug("Left room")
            self._last_room = current_room
    
    def render(self):
        """Render the game state to the screen."""
        # Clear the screen
        self.screen.fill(COLOR_WHITE)
        
        # Only render game world when playing or paused
        if self.state in [GameState.PLAYING, GameState.PAUSED]:
            # Draw the tilemap
            self.tilemap.draw(self.screen)
            
            # Draw the player
            self.player.draw(self.screen)
            
            # Draw semi-transparent overlay when paused
            if self.state == GameState.PAUSED:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(128)
                self.screen.blit(overlay, (0, 0))
        
        # Draw UI
        self.ui_manager.draw_ui(self.screen)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Run the main game loop."""
        logger.info("Starting game loop")
        
        while self.is_running:
            # Calculate delta time
            delta_time = self.clock.tick(60) / 1000.0
            
            self.handle_events()
            self.update(delta_time)
            self.render()
        
        logger.info("Game loop ended")
        pygame.quit()
        sys.exit()

def main():
    """Entry point for the game."""
    try:
        game = Game()
        game.run()
    except Exception as e:
        logger.exception("Game crashed")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main() 