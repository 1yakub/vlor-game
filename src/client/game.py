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
    COLOR_BLACK
)
from shared.logger import get_logger
from client.player import Player

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
        
        # Create UI manager
        self.ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Create player at center of screen
        self.player = Player(
            position=Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
            color=COLOR_BLACK
        )
        
        logger.info("Game initialized successfully")
    
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            # Handle UI events
            self.ui_manager.process_events(event)
            
            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
    
    def update(self, delta_time: float):
        """Update game state.
        
        Args:
            delta_time: Time elapsed since last update in seconds
        """
        # Handle player input and update
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(delta_time)
        
        # Update UI
        self.ui_manager.update(delta_time)
    
    def render(self):
        """Render the game state to the screen."""
        # Clear the screen
        self.screen.fill(COLOR_WHITE)
        
        # Draw the player
        self.player.draw(self.screen)
        
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