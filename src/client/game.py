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
    ASSET_DIR,
    BusinessType,
    PlayerRole,
    ConflictType,
    TILE_SIZE
)
from shared.logger import get_logger
from client.player import Player
from client.tilemap import create_test_map
from client.ui.menu import MenuManager
from client.ui.business import BusinessPanel
from client.ui.trading import TradingPanel
from client.ui.mediation import MediationPanel
from client.business import BusinessManager

logger = get_logger(__name__)

class Game:
    """Main game class handling the game loop and core functionality."""
    
    # Singleton instance
    instance = None
    
    def __init__(self):
        """Initialize the game engine and create the game window."""
        if Game.instance is not None:
            raise RuntimeError("Game instance already exists")
        Game.instance = self
        
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
        
        # Create managers
        self.menu_manager = MenuManager(self.ui_manager)
        self.business_manager = BusinessManager()
        
        # Create UI panels
        self.business_panel = BusinessPanel(self.ui_manager)
        self.trading_panel = TradingPanel(self.ui_manager)
        self.mediation_panel = MediationPanel(self.ui_manager)
        
        # Create camera offset
        self.camera_offset = pygame.Vector2(0, 0)
        
        # Create tilemap
        self.tilemap = create_test_map()
        
        # Create player at center of screen
        self.player = Player(
            position=Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        
        # Create test businesses
        self._create_test_businesses()
        
        logger.info("Game initialized successfully")
    
    def _create_test_businesses(self):
        """Create test businesses for development."""
        # Create a retail business
        retail = self.business_manager.create_business(
            name="Varygen Mart",
            type=BusinessType.RETAIL,
            owner="Player1"
        )
        retail.add_resource("Electronics", 100, 50.0)
        retail.add_resource("Furniture", 50, 200.0)
        
        # Create a manufacturing business
        manufacturing = self.business_manager.create_business(
            name="Varygen Industries",
            type=BusinessType.MANUFACTURING,
            owner="Player2"
        )
        manufacturing.add_resource("Raw Materials", 500, 20.0)
        manufacturing.add_resource("Machinery", 10, 1000.0)
        
        # Create a test contract
        self.business_manager.create_contract(
            seller=manufacturing,
            buyer=retail,
            resource="Raw Materials",
            quantity=50,
            price=1500.0
        )
        
        # Create a test conflict
        self.business_manager.create_conflict(
            type=ConflictType.CONTRACT_BREACH,
            description="Failed to deliver raw materials on time",
            parties=[retail, manufacturing]
        )
        
        # Create another test conflict
        self.business_manager.create_conflict(
            type=ConflictType.RESOURCE_DISPUTE,
            description="Dispute over machinery maintenance costs",
            parties=[manufacturing, retail]
        )
        
        # Show the retail business panel for testing
        self.business_panel.show(retail)
    
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            # Handle UI events
            self.ui_manager.process_events(event)
            self.menu_manager.handle_event(event)
            self.business_panel.handle_event(event)
            self.trading_panel.handle_event(event)
            
            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                        self.menu_manager.show_state(GameState.PAUSED)
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                        self.menu_manager.show_state(GameState.PLAYING)
                elif event.key == pygame.K_b and self.state == GameState.PLAYING:
                    # Toggle business panel
                    if self.business_panel.visible:
                        self.business_panel.hide()
                    else:
                        # Show panel for first business (for testing)
                        first_business = next(iter(self.business_manager.businesses.values()))
                        self.business_panel.show(first_business)
                elif event.key == pygame.K_t and self.state == GameState.PLAYING:
                    # Show trading panel (for testing)
                    if not self.trading_panel.visible:
                        businesses = list(self.business_manager.businesses.values())
                        if len(businesses) >= 2:
                            self.trading_panel.show(businesses[0], businesses[1])
                elif event.key == pygame.K_m and self.state == GameState.PLAYING:
                    # Show mediation panel for first unresolved conflict (for testing)
                    for business in self.business_manager.businesses.values():
                        for conflict in business.conflicts:
                            if not conflict.is_resolved:
                                self.mediation_panel.show(conflict)
                                break
                        if self.mediation_panel.visible:
                            break
    
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
            
            # Update camera to follow player
            target_x = self.player.position.x - WINDOW_WIDTH // 2
            target_y = self.player.position.y - WINDOW_HEIGHT // 2
            
            # Clamp camera to map bounds
            max_x = self.tilemap.width * TILE_SIZE - WINDOW_WIDTH
            max_y = self.tilemap.height * TILE_SIZE - WINDOW_HEIGHT
            
            self.camera_offset.x = max(0, min(target_x, max_x))
            self.camera_offset.y = max(0, min(target_y, max_y))
            
            # Log room changes for debugging
            current_room = self.tilemap.get_room_at(self.player.position)
            if hasattr(self, '_last_room') and self._last_room != current_room:
                if current_room:
                    logger.debug(f"Entered room: {current_room.name} ({current_room.room_type})")
                else:
                    logger.debug("Left room")
            self._last_room = current_room
            
            # Update business system
            self.business_manager.update(delta_time)
            
            # Update UI panels
            if self.business_panel.visible:
                self.business_panel.update_display()
            if self.trading_panel.visible:
                self.trading_panel.update_display()
            if self.mediation_panel.visible:
                self.mediation_panel.handle_event(pygame.event.Event(pygame.USEREVENT))
    
    def render(self):
        """Render the game state to the screen."""
        # Clear the screen
        self.screen.fill(COLOR_WHITE)
        
        # Only render game world when playing or paused
        if self.state in [GameState.PLAYING, GameState.PAUSED]:
            # Draw the tilemap with camera offset
            self.tilemap.draw(self.screen, (int(self.camera_offset.x), int(self.camera_offset.y)))
            
            # Draw the player with camera offset
            player_screen_pos = self.player.position - self.camera_offset
            self.player.draw(self.screen, player_screen_pos)
            
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